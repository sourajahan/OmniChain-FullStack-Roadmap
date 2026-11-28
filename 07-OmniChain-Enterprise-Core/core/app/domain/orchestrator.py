from dataclasses import asdict, dataclass
from typing import Any
import uuid

from app.domain.events import EventBus
from app.domain.inventory import InventoryService
from app.domain.logistics import LogisticsService


class PaymentError(Exception):
    pass


@dataclass
class EnterpriseOrder:
    order_id: str
    customer_id: str
    sku: str
    quantity: int
    destination_region: str
    unit_price_usd: float
    total_usd: float
    status: str
    warehouse_id: str | None = None
    tracking_code: str | None = None
    failure_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class OrderOrchestrator:
    """Saga-ready order orchestrator with idempotency and compensating inventory rollback."""

    def __init__(
        self,
        inventory: InventoryService,
        logistics: LogisticsService,
        events: EventBus,
    ) -> None:
        self.inventory = inventory
        self.logistics = logistics
        self.events = events
        self._orders: dict[str, EnterpriseOrder] = {}
        self._idempotency: dict[str, str] = {}

    def create_order(
        self,
        customer_id: str,
        sku: str,
        quantity: int,
        destination_region: str,
        unit_price_usd: float,
        idempotency_key: str | None = None,
        simulate_payment_failure: bool = False,
    ) -> tuple[dict[str, Any], bool]:
        if idempotency_key and idempotency_key in self._idempotency:
            existing_id = self._idempotency[idempotency_key]
            return self._orders[existing_id].to_dict(), True

        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        total_usd = round(quantity * unit_price_usd, 2)
        order = EnterpriseOrder(
            order_id=order_id,
            customer_id=customer_id,
            sku=sku,
            quantity=quantity,
            destination_region=destination_region,
            unit_price_usd=unit_price_usd,
            total_usd=total_usd,
            status="PENDING",
        )
        self.events.publish("OrderCreated", order_id, {"sku": sku, "quantity": quantity, "total_usd": total_usd})

        # Step 1: Reserve Inventory across multi-warehouse pool
        warehouse_id = self.inventory.reserve_stock(sku=sku, quantity=quantity, preferred_region=destination_region)
        order.warehouse_id = warehouse_id
        self.events.publish("InventoryReserved", order_id, {"warehouse_id": warehouse_id, "sku": sku, "quantity": quantity})

        try:
            # Step 2: Capture Payment
            if simulate_payment_failure:
                raise PaymentError("Payment gateway declined transaction")
            self.events.publish("PaymentCaptured", order_id, {"amount_usd": total_usd})

            # Step 3: Dispatch Cloud Logistics Shipment
            shipment = self.logistics.dispatch(
                order_id=order_id,
                warehouse_id=warehouse_id,
                destination_region=destination_region,
                quantity=quantity,
            )
            order.tracking_code = str(shipment["tracking_code"])
            order.status = "CONFIRMED"
            self.events.publish("ShipmentDispatched", order_id, shipment)
        except Exception as exc:
            # Compensating transaction: release reserved stock
            self.inventory.release_stock(warehouse_id=warehouse_id, sku=sku, quantity=quantity)
            order.status = "COMPENSATED"
            order.failure_reason = str(exc)
            self.events.publish(
                "OrderCompensated",
                order_id,
                {"warehouse_id": warehouse_id, "sku": sku, "quantity": quantity, "reason": str(exc)},
            )

        self._orders[order_id] = order
        if idempotency_key:
            self._idempotency[idempotency_key] = order_id
        return order.to_dict(), False

    def get_order(self, order_id: str) -> dict[str, Any] | None:
        order = self._orders.get(order_id)
        return order.to_dict() if order else None
