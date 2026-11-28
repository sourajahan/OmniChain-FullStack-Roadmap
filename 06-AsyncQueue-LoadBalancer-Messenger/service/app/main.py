from typing import Any

from fastapi import FastAPI, Header, HTTPException, Response
from pydantic import BaseModel, Field

from app.broker import QueueBroker
from app.config import Settings, settings
from app.worker import process_next_job


class MessageRequest(BaseModel):
    channel: str = Field(pattern="^(email|sms|webhook|push)$")
    recipient: str = Field(min_length=3, max_length=200)
    payload: dict[str, Any] = Field(default_factory=dict)


def create_app(cfg: Settings | None = None, broker: QueueBroker | None = None) -> FastAPI:
    active_cfg = cfg or settings
    active_broker = broker or QueueBroker(active_cfg.redis_url, active_cfg.queue_name, active_cfg.dlq_name)
    app = FastAPI(title="AsyncQueue LoadBalancer Messenger", version="1.0.0")

    @app.middleware("http")
    async def attach_instance_header(request, call_next):  # type: ignore[no-untyped-def]
        response = await call_next(request)
        response.headers["X-Upstream-Instance"] = active_cfg.instance_id
        return response

    @app.get("/health")
    def health() -> dict[str, object]:
        return {"status": "ok", "instance": active_cfg.instance_id, "stats": active_broker.stats()}

    @app.post("/api/v1/messages", status_code=202)
    def enqueue_message(
        req: MessageRequest,
        response: Response,
        idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    ) -> dict[str, Any]:
        job, deduplicated = active_broker.enqueue(
            channel=req.channel,
            recipient=req.recipient,
            payload=req.payload,
            idempotency_key=idempotency_key,
        )
        response.headers["X-Idempotent-Replay"] = "true" if deduplicated else "false"
        return job

    @app.get("/api/v1/messages/{job_id}")
    def get_message_status(job_id: str) -> dict[str, Any]:
        job = active_broker.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

    @app.post("/api/v1/dlq/replay")
    def replay_dead_letters() -> dict[str, int]:
        return {"replayed": active_broker.replay_dlq()}

    @app.post("/api/v1/worker/drain")
    def drain_one() -> dict[str, Any]:
        job = process_next_job(active_broker, max_retries=active_cfg.max_retries)
        return {"processed": job}

    return app


app = create_app()
