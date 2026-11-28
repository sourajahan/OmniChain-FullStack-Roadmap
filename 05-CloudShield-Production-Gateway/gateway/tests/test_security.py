import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def test_owasp_security_headers_and_cdn_cache_control() -> None:
    app = create_app(Settings(rate_limit_requests=10, rate_limit_window_seconds=60))
    client = TestClient(app)

    res = client.get("/api/v1/public/catalog")
    assert res.status_code == 200
    assert "max-age=63072000" in res.headers["Strict-Transport-Security"]
    assert res.headers["X-Content-Type-Options"] == "nosniff"
    assert res.headers["X-Frame-Options"] == "DENY"
    assert "default-src 'none'" in res.headers["Content-Security-Policy"]
    assert "public, max-age=300" in res.headers["Cache-Control"]
    assert "X-Request-ID" in res.headers


def test_rate_limiting_returns_429_with_retry_after() -> None:
    app = create_app(Settings(rate_limit_requests=2, rate_limit_window_seconds=60))
    client = TestClient(app)

    assert client.get("/health").status_code == 200
    assert client.get("/health").status_code == 200

    blocked = client.get("/health")
    assert blocked.status_code == 429
    assert blocked.headers["X-RateLimit-Remaining"] == "0"
    assert int(blocked.headers["Retry-After"]) >= 1


def test_production_rejects_weak_default_secret() -> None:
    with pytest.raises(ValueError, match="Production requires a strong API_SECRET_KEY"):
        Settings(app_env="production", api_secret_key="dev-only-change-in-production-32chars")


def test_admin_endpoint_requires_valid_secret() -> None:
    secret = "a" * 32
    app = create_app(Settings(app_env="production", api_secret_key=secret))
    client = TestClient(app)

    assert client.get("/api/v1/admin/audit").status_code == 401
    ok = client.get("/api/v1/admin/audit", headers={"X-API-Key": secret})
    assert ok.status_code == 200
    assert ok.json()["audit"] == "verified"
