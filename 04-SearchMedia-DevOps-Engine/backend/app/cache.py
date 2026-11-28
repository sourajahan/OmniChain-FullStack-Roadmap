import json
from typing import Any

import redis


class CacheService:
    VERSION_KEY = "media:cache_version"

    def __init__(self, redis_url: str, ttl_seconds: int = 60, client: Any | None = None) -> None:
        self.ttl_seconds = ttl_seconds
        self._client = client if client is not None else redis.Redis.from_url(
            redis_url, decode_responses=True, socket_connect_timeout=1, socket_timeout=1
        )

    def get_version(self) -> int | None:
        try:
            val = self._client.get(self.VERSION_KEY)
            return int(val) if val is not None else 1
        except Exception:
            return None

    def bump_version(self) -> None:
        try:
            self._client.incr(self.VERSION_KEY)
        except Exception:
            pass

    def build_search_key(self, version: int, q: str, page: int, limit: int) -> str:
        normalized_q = q.strip().lower()
        return f"media:search:v{version}:q={normalized_q}:p={page}:l={limit}"

    def get_json(self, key: str) -> dict[str, Any] | None:
        try:
            raw = self._client.get(key)
            return json.loads(raw) if raw else None
        except Exception:
            return None

    def set_json(self, key: str, payload: dict[str, Any]) -> None:
        try:
            self._client.setex(key, self.ttl_seconds, json.dumps(payload))
        except Exception:
            pass

    def ping(self) -> bool:
        try:
            return bool(self._client.ping())
        except Exception:
            return False
