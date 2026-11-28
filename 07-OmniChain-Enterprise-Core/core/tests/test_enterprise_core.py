from fastapi.testclient import TestClient

from app.main import create_app


def test_order_orchestration_idempotency_and_shipment_lifecycle() -> None:
    client = TestClient(create_app())

    payload = {
        "customer_id": "CUST-900",
        "sku": "SKU-LAPTOP-PRO",
        "quantity": 2,
        "destination_region": "EU",
        "unit_price_usd": 1499.0,
    }
    first = client.post("/api/v1/orders", json=payload, headers={"Idempotency-Key": "order-key-1"})
    second = client.post("/api/v1/orders", json=payload, headers={"Idempotency-Key": "order-key-1"})

    assert first.status_code == 201
    assert first.headers["X-Idempotent-Replay"] == "false"
    assert second.headers["X-Idempotent-Replay"] == "true"

    order = first.json()
    assert order["order_id"] == second.json()["order_id"]
    assert order["status"] == "CONFIRMED"
    assert order["warehouse_id"] == "WH-EU-1"
    tracking = order["tracking_code"]
    assert tracking.startswith("TRK-")

    # Advance shipment lifecycle: DISPATCHED -> IN_TRANSIT -> DELIVERED
    t1 = client.patch(f"/api/v1/shipments/{tracking}/status", json={"status": "IN_TRANSIT"})
    assert t1.status_code == 200 and t1.json()["status"] == "IN_TRANSIT"

    t2 = client.patch(f"/api/v1/shipments/{tracking}/status", json={"status": "DELIVERED"})
    assert t2.status_code == 200 and t2.json()["status"] == "DELIVERED"

    # Verify immutable domain events were recorded
    events = client.get("/api/v1/events", params={"aggregate_id": order["order_id"]}).json()
    event_types = [e["event_type"] for e in events]
    assert event_types == ["OrderCreated", "InventoryReserved", "PaymentCaptured", "ShipmentDispatched"]


def test_payment_failure_triggers_automatic_inventory_compensation() -> None:
    client = TestClient(create_app())

    before = {f"{s['warehouse_id']}:{s['sku']}": s["available"] for s in client.get("/api/v1/inventory").json()}
    res = client.post(
        "/api/v1/orders",
        json={
            "customer_id": "CUST-901",
            "sku": "SKU-SERVER-RACK",
            "quantity": 3,
            "destination_region": "EU",
            "unit_price_usd": 4200.0,
            "simulate_payment_failure": True,
        },
    )
    assert res.status_code == 201
    order = res.json()
    assert order["status"] == "COMPENSATED"
    assert order["tracking_code"] is None

    after = {f"{s['warehouse_id']}:{s['sku']}": s["available"] for s in client.get("/api/v1/inventory").json()}
    assert after["WH-EU-1:SKU-SERVER-RACK"] == before["WH-EU-1:SKU-SERVER-RACK"]

    events = client.get("/api/v1/events", params={"aggregate_id": order["order_id"]}).json()
    assert events[-1]["event_type"] == "OrderCompensated"


def test_insufficient_stock_returns_409() -> None:
    client = TestClient(create_app())
    res = client.post(
        "/api/v1/orders",
        json={
            "customer_id": "CUST-902",
            "sku": "SKU-SERVER-RACK",
            "quantity": 50,
            "destination_region": "EU",
            "unit_price_usd": 4200.0,
        },
    )
    assert res.status_code == 409
