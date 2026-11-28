from dataclasses import asdict, dataclass
import uuid


VALID_TRANSITIONS = {
    "DISPATCHED": {"IN_TRANSIT"},
    "IN_TRANSIT": {"DELIVERED"},
    "DELIVERED": set(),
}


@dataclass
class Shipment:
    tracking_code: str
    order_id: str
    warehouse_id: str
    destination_region: str
    carrier: str
    shipping_cost_usd: float
    status: str = "DISPATCHED"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class LogisticsService:
    """Cloud logistics engine with carrier routing and shipment lifecycle tracking."""

    def __init__(self) -> None:
        self._shipments: dict[str, Shipment] = {}

    def dispatch(self, order_id: str, warehouse_id: str, destination_region: str, quantity: int) -> dict[str, object]:
        carrier = "DHL-Express-EU" if destination_region == "EU" else "FedEx-Global-Air"
        base_rate = 14.5 if destination_region == "EU" else 22.0
        cost = round(base_rate + (quantity * 2.5), 2)
        tracking = f"TRK-{uuid.uuid4().hex[:10].upper()}"
        shipment = Shipment(
            tracking_code=tracking,
            order_id=order_id,
            warehouse_id=warehouse_id,
            destination_region=destination_region,
            carrier=carrier,
            shipping_cost_usd=cost,
        )
        self._shipments[tracking] = shipment
        return shipment.to_dict()

    def advance_status(self, tracking_code: str, next_status: str) -> dict[str, object]:
        shipment = self._shipments.get(tracking_code)
        if not shipment:
            raise KeyError("Shipment not found")
        if next_status not in VALID_TRANSITIONS.get(shipment.status, set()):
            raise ValueError(f"Invalid transition from {shipment.status} to {next_status}")
        shipment.status = next_status
        return shipment.to_dict()

    def get_shipment(self, tracking_code: str) -> dict[str, object] | None:
        shipment = self._shipments.get(tracking_code)
        return shipment.to_dict() if shipment else None
