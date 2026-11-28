import json
import uuid
from collections import deque
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

import redis


@dataclass
class MessageJob:
    job_id: str
    channel: str
    recipient: str
    payload: dict[str, Any]
    status: str = "queued"
    attempts: int = 0
    last_error: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class QueueBroker:
    """Redis-backed queue broker with seamless in-memory fallback for isolated testing."""

    def __init__(self, redis_url: str = "", queue_name: str = "omnichain:messages", dlq_name: str = "omnichain:messages:dlq") -> None:
        self.queue_name = queue_name
        self.dlq_name = dlq_name
        self._client: redis.Redis | None = None  # type: ignore[type-arg]
        if redis_url:
            try:
                client = redis.from_url(redis_url, decode_responses=True, socket_connect_timeout=1)
                client.ping()
                self._client = client
            except Exception:
                self._client = None

        self._queue: deque[str] = deque()
        self._dlq: deque[str] = deque()
        self._jobs: dict[str, dict[str, Any]] = {}
        self._idempotency: dict[str, str] = {}

    def enqueue(self, channel: str, recipient: str, payload: dict[str, Any], idempotency_key: str | None = None) -> tuple[dict[str, Any], bool]:
        if idempotency_key:
            existing_id = self._get_idempotency(idempotency_key)
            if existing_id:
                existing = self.get_job(existing_id)
                if existing:
                    return existing, True

        job = MessageJob(job_id=str(uuid.uuid4()), channel=channel, recipient=recipient, payload=payload)
        data = job.to_dict()
        self._save_job(job.job_id, data)
        if idempotency_key:
            self._set_idempotency(idempotency_key, job.job_id)

        if self._client:
            self._client.rpush(self.queue_name, job.job_id)
        else:
            self._queue.append(job.job_id)
        return data, False

    def dequeue(self) -> dict[str, Any] | None:
        job_id = self._client.lpop(self.queue_name) if self._client else (self._queue.popleft() if self._queue else None)
        if not job_id:
            return None
        return self.get_job(str(job_id))

    def requeue(self, job: dict[str, Any]) -> None:
        self._save_job(job["job_id"], job)
        if self._client:
            self._client.rpush(self.queue_name, job["job_id"])
        else:
            self._queue.append(job["job_id"])

    def move_to_dlq(self, job: dict[str, Any]) -> None:
        job["status"] = "dead_letter"
        self._save_job(job["job_id"], job)
        if self._client:
            self._client.rpush(self.dlq_name, job["job_id"])
        else:
            self._dlq.append(job["job_id"])

    def replay_dlq(self) -> int:
        replayed = 0
        while True:
            job_id = self._client.lpop(self.dlq_name) if self._client else (self._dlq.popleft() if self._dlq else None)
            if not job_id:
                break
            job = self.get_job(str(job_id))
            if job:
                job["status"] = "queued"
                job["attempts"] = 0
                job["last_error"] = None
                self.requeue(job)
                replayed += 1
        return replayed

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        if self._client:
            raw = self._client.get(f"job:{job_id}")
            return json.loads(raw) if raw else None
        return self._jobs.get(job_id)

    def save_job(self, job: dict[str, Any]) -> None:
        self._save_job(job["job_id"], job)

    def stats(self) -> dict[str, int]:
        if self._client:
            return {
                "queued": int(self._client.llen(self.queue_name)),
                "dlq": int(self._client.llen(self.dlq_name)),
            }
        return {"queued": len(self._queue), "dlq": len(self._dlq)}

    def _save_job(self, job_id: str, data: dict[str, Any]) -> None:
        if self._client:
            self._client.set(f"job:{job_id}", json.dumps(data))
        else:
            self._jobs[job_id] = data

    def _get_idempotency(self, key: str) -> str | None:
        if self._client:
            val = self._client.get(f"idem:{key}")
            return str(val) if val else None
        return self._idempotency.get(key)

    def _set_idempotency(self, key: str, job_id: str) -> None:
        if self._client:
            self._client.set(f"idem:{key}", job_id, ex=3600)
        else:
            self._idempotency[key] = job_id
