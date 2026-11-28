from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from app.cache import CacheService
from app.main import create_app
from app.store import MediaRepository


class FakeRedis:
    def __init__(self) -> None:
        self.store: dict[str, Any] = {}

    def get(self, key: str) -> str | None:
        val = self.store.get(key)
        return str(val) if val is not None else None

    def setex(self, key: str, _ttl: int, value: str) -> None:
        self.store[key] = value

    def incr(self, key: str) -> int:
        val = int(self.store.get(key, 1)) + 1
        self.store[key] = val
        return val

    def ping(self) -> bool:
        return True


def make_client(tmp_path: Path) -> TestClient:
    repo = MediaRepository(str(tmp_path / "test.db"))
    cache = CacheService("redis://unused", ttl_seconds=60, client=FakeRedis())
    app = create_app(repo=repo, cache=cache, upload_dir=str(tmp_path / "uploads"))
    return TestClient(app)


def test_health_endpoint(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "redis": "connected"}


def test_upload_validation_rejects_unsupported_mime(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    res = client.post(
        "/api/v1/media/upload",
        data={"title": "Malicious Script", "tags": "bad"},
        files={"file": ("script.sh", b"#!/bin/sh", "application/x-sh")},
    )
    assert res.status_code == 415


def test_upload_search_pagination_and_redis_cache_invalidation(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    for i in range(3):
        res = client.post(
            "/api/v1/media/upload",
            data={"title": f"Architecture Doc {i}", "tags": "devops,redis"},
            files={"file": (f"doc_{i}.txt", f"hello {i}".encode(), "text/plain")},
        )
        assert res.status_code == 201

    res1 = client.get("/api/v1/media?q=Architecture&page=1&limit=2")
    assert res1.status_code == 200
    assert res1.headers["X-Cache"] == "MISS"
    body1 = res1.json()
    assert body1["total"] == 3
    assert len(body1["items"]) == 2
    assert body1["pages"] == 2

    res2 = client.get("/api/v1/media?q=Architecture&page=1&limit=2")
    assert res2.status_code == 200
    assert res2.headers["X-Cache"] == "HIT"

    item_id = body1["items"][0]["id"]
    del_res = client.delete(f"/api/v1/media/{item_id}")
    assert del_res.status_code == 204

    res3 = client.get("/api/v1/media?q=Architecture&page=1&limit=2")
    assert res3.status_code == 200
    assert res3.headers["X-Cache"] == "MISS"
    assert res3.json()["total"] == 2
