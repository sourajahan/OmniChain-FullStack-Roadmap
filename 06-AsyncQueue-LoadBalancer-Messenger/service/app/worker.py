import time
from typing import Any, Callable

from app.broker import QueueBroker
from app.config import settings


def default_deliver(job: dict[str, Any]) -> None:
    if job["payload"].get("simulate_failure"):
        raise RuntimeError("Simulated downstream provider outage")


def process_next_job(
    broker: QueueBroker,
    max_retries: int = 3,
    deliver_fn: Callable[[dict[str, Any]], None] = default_deliver,
) -> dict[str, Any] | None:
    job = broker.dequeue()
    if not job:
        return None

    job["attempts"] = int(job.get("attempts", 0)) + 1
    try:
        deliver_fn(job)
        job["status"] = "delivered"
        job["last_error"] = None
        broker.save_job(job)
    except Exception as exc:
        job["last_error"] = str(exc)
        if job["attempts"] >= max_retries:
            broker.move_to_dlq(job)
        else:
            job["status"] = "retrying"
            broker.requeue(job)
    return job


def run_worker_loop() -> None:
    broker = QueueBroker(settings.redis_url, settings.queue_name, settings.dlq_name)
    while True:
        processed = process_next_job(broker, max_retries=settings.max_retries)
        if not processed:
            time.sleep(0.25)


if __name__ == "__main__":
    run_worker_loop()
