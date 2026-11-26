from uuid import uuid4

from fastapi.testclient import TestClient

from coreauth.api.main import app
from coreauth.infra.db import SessionLocal
from coreauth.infra.models import User, UserRole

client = TestClient(app)


def _cleanup_user(email: str) -> None:
    db = SessionLocal()
    try:
        db.query(User).filter(User.email == email).delete(synchronize_session=False)
        db.commit()
    finally:
        db.close()


def test_full_auth_lifecycle_and_replay_detection() -> None:
    email = f"auth-{uuid4().hex[:8]}@example.com"
    password = "StrongPassword!2026"

    try:
        # 1. Register
        reg = client.post("/api/v1/auth/register", json={"email": email, "password": password})
        assert reg.status_code == 201
        assert reg.json()["email"] == email
        assert reg.json()["role"] == "customer"
        assert "password_hash" not in reg.json()

        # 2. Duplicate register -> 409
        dup = client.post("/api/v1/auth/register", json={"email": email, "password": password})
        assert dup.status_code == 409

        # 3. Login
        login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
        assert login.status_code == 200
        tokens1 = login.json()
        assert tokens1["access_token"]
        assert tokens1["refresh_token"]

        # 4. Access /me with Bearer token
        me = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {tokens1['access_token']}"},
        )
        assert me.status_code == 200
        assert me.json()["email"] == email

        # 5. RBAC: Customer blocked from admin-only (403)
        forbidden = client.get(
            "/api/v1/auth/admin-only",
            headers={"Authorization": f"Bearer {tokens1['access_token']}"},
        )
        assert forbidden.status_code == 403

        # 6. Refresh token rotation
        ref = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": tokens1["refresh_token"]},
        )
        assert ref.status_code == 200
        tokens2 = ref.json()
        assert tokens2["refresh_token"] != tokens1["refresh_token"]

        # 7. Replay Attack: Reusing old refresh token revokes the entire family!
        replay = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": tokens1["refresh_token"]},
        )
        assert replay.status_code == 401

        # Even the newer token in the same family must now be revoked
        revoked_new = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": tokens2["refresh_token"]},
        )
        assert revoked_new.status_code == 401
    finally:
        _cleanup_user(email)


def test_rbac_allows_admin_role() -> None:
    email = f"admin-{uuid4().hex[:8]}@example.com"
    password = "AdminPassword!2026"

    try:
        reg = client.post("/api/v1/auth/register", json={"email": email, "password": password})
        assert reg.status_code == 201

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).one()
            user.role = UserRole.ADMIN
            db.commit()
        finally:
            db.close()

        login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
        token = login.json()["access_token"]

        allowed = client.get(
            "/api/v1/auth/admin-only",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert allowed.status_code == 200
        assert allowed.json() == {"message": "welcome admin"}
    finally:
        _cleanup_user(email)
