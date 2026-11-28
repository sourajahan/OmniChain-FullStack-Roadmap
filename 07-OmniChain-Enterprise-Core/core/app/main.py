from typing import Any

from fastapi import FastAPI, Header, HTTPException, Response
from pydantic import BaseModel, Field

from app.domain.events import EventBus
from app.domain.inventory import InventoryError, InventoryService
from app.domain.logistics import LogisticsService
from app.domain.orchestrator import OrderOrchestrator


class CreateOrderRequest(BaseModel):
    customer_id: str = Field(min_length=2, max_length=64)
    sku: str = Field(min_length=3, max_length=64)
    quantity: int = Field(gt=0, le=100)
    destination_region: str = Field(pattern="^(EU|US|APAC)$")
    unit_price_usd: float = Field(gt=0)
    simulate_payment_failure: bool = False


class AdvanceShipmentRequest(BaseModel):
    status: str = Field(pattern="^(IN_TRANSIT|DELIVERED)$")


def create_app() -> FastAPI:
    events = EventBus()
    inventory = InventoryService()
    logistics = LogisticsService()
    orchestrator = OrderOrchestrator(inventory=inventory, logistics=logistics, events=events)

    app = FastAPI(title="OmniChain Enterprise Core", version="1.0.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "omnichain-enterprise-core"}

    @app.get("/api/v1/inventory")
    def list_inventory() -> list[dict[str, object]]:
        return inventory.list_stock()

    @app.post("/api/v1/orders", status_code=201)
    def create_order(
        req: CreateOrderRequest,
        response: Response,
        idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    ) -> dict[str, Any]:
        try:
            order, replayed = orchestrator.create_order(
                customer_id=req.customer_id,
                sku=req.sku,
                quantity=req.quantity,
                destination_region=req.destination_region,
                unit_price_usd=req.unit_price_usd,
                idempotency_key=idempotency_key,
                simulate_payment_failure=req.simulate_payment_failure,
            )
        except InventoryError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

        response.headers["X-Idempotent-Replay"] = "true" if replayed else "false"
        return order

    @app.get("/api/v1/orders/{order_id}")
    def get_order(order_id: str) -> dict[str, Any]:
        order = orchestrator.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    @app.get("/api/v1/shipments/{tracking_code}")
    def get_shipment(tracking_code: str) -> dict[str, object]:
        shipment = logistics.get_shipment(tracking_code)
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        return shipment

    @app.patch("/api/v1/shipments/{tracking_code}/status")
    def advance_shipment(tracking_code: str, req: AdvanceShipmentRequest) -> dict[str, object]:
        try:
            updated = logistics.advance_status(tracking_code, req.status)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Shipment not found") from exc
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        events.publish("ShipmentStatusUpdated", tracking_code, updated)
        return updated

    @app.get("/api/v1/events")
    def list_events(aggregate_id: str | None = None) -> list[dict[str, Any]]:
        return events.list_events(aggregate_id=aggregate_id)

    return app


app = create_app()
