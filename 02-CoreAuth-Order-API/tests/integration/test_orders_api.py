from uuid import uuid4

from fastapi.testclient import TestClient

from coreauth.api.main import app
from coreauth.infra.db import SessionLocal
from coreauth.infra.models import Order, User, UserRole

client = TestClient(app)


def _create_user_and_token(role: UserRole = UserRole.CUSTOMER) -> tuple[str, str]:
    email = f"{role.value}-{uuid4().hex[:8]}@example.com"
    password = "StrongPassword!2026"
    reg = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert reg.status_code == 201

    if role != UserRole.CUSTOMER:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).one()
            user.role = role
            db.commit()
        finally:
            db.close()

    login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    return email, login.json()["access_token"]


def _cleanup(emails: list[str], order_ids: list[int]) -> None:
    db = SessionLocal()
    try:
        if order_ids:
            db.query(Order).filter(Order.id.in_(order_ids)).delete(synchronize_session=False)
        if emails:
            db.query(User).filter(User.email.in_(emails)).delete(synchronize_session=False)
        db.commit()
    finally:
        db.close()


def test_orders_lifecycle_idor_and_state_machine() -> None:
    emails: list[str] = []
    order_ids: list[int] = []

    try:
        email_a, token_a = _create_user_and_token(UserRole.CUSTOMER)
        email_b, token_b = _create_user_and_token(UserRole.CUSTOMER)
        email_wh, token_wh = _create_user_and_token(UserRole.WAREHOUSE)
        emails.extend([email_a, email_b, email_wh])

        # 1. Customer A creates an order
        create_resp = client.post(
            "/api/v1/orders",
            headers={"Authorization": f"Bearer {token_a}"},
            json={
                "items": [
                    {"sku": "SKU-LAPTOP", "quantity": 2, "unit_price": "1250.50"},
                    {"sku": "SKU-MOUSE", "quantity": 1, "unit_price": "49.00"},
                ]
            },
        )
        assert create_resp.status_code == 201
        order = create_resp.json()
        order_ids.append(order["id"])
        assert order["status"] == "pending"
        assert order["total_amount"] == "2550.00"
        assert len(order["items"]) == 2

        # 2. IDOR Protection: Customer B cannot view Customer A's order (403 + RFC 7807)
        idor_resp = client.get(
            f"/api/v1/orders/{order['id']}",
            headers={"Authorization": f"Bearer {token_b}"},
        )
        assert idor_resp.status_code == 403
        assert idor_resp.headers["content-type"].startswith("application/problem+json")
        problem = idor_resp.json()
        assert problem["status"] == 403
        assert "correlation_id" in problem

        # 3. RBAC: Customer A cannot update order status (403)
        cust_patch = client.patch(
            f"/api/v1/orders/{order['id']}/status",
            headers={"Authorization": f"Bearer {token_a}"},
            json={"status": "paid"},
        )
        assert cust_patch.status_code == 403

        # 4. Warehouse transitions pending -> paid -> shipped
        paid_resp = client.patch(
            f"/api/v1/orders/{order['id']}/status",
            headers={"Authorization": f"Bearer {token_wh}"},
            json={"status": "paid"},
        )
        assert paid_resp.status_code == 200
        assert paid_resp.json()["status"] == "paid"

        shipped_resp = client.patch(
            f"/api/v1/orders/{order['id']}/status",
            headers={"Authorization": f"Bearer {token_wh}"},
            json={"status": "shipped"},
        )
        assert shipped_resp.status_code == 200
        assert shipped_resp.json()["status"] == "shipped"

        # 5. State Machine: shipped -> cancelled is forbidden (409)
        invalid_resp = client.patch(
            f"/api/v1/orders/{order['id']}/status",
            headers={"Authorization": f"Bearer {token_wh}"},
            json={"status": "cancelled"},
        )
        assert invalid_resp.status_code == 409
    finally:
        _cleanup(emails, order_ids)
