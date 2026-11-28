from fastapi.testclient import TestClient

from app.broker import QueueBroker
from app.config import Settings
from app.main import create_app
from app.worker import process_next_job


def test_idempotent_enqueue_and_worker_delivery() -> None:
    broker = QueueBroker()
    app = create_app(Settings(instance_id="api-test-1", max_retries=2), broker=broker)
    client = TestClient(app)

    payload = {"channel": "email", "recipient": "ops@omnichain.dev", "payload": {"subject": "Order #101"}}
    first = client.post("/api/v1/messages", json=payload, headers={"Idempotency-Key": "idem-101"})
    second = client.post("/api/v1/messages", json=payload, headers={"Idempotency-Key": "idem-101"})

    assert first.status_code == 202
    assert first.headers["X-Upstream-Instance"] == "api-test-1"
    assert first.headers["X-Idempotent-Replay"] == "false"
    assert second.headers["X-Idempotent-Replay"] == "true"
    assert first.json()["job_id"] == second.json()["job_id"]
    assert broker.stats()["queued"] == 1

    processed = process_next_job(broker, max_retries=2)
    assert processed is not None
    assert processed["status"] == "delivered"
    assert broker.stats()["queued"] == 0


def test_retries_dlq_and_replay() -> None:
    broker = QueueBroker()
    app = create_app(Settings(max_retries=2), broker=broker)
    client = TestClient(app)

    res = client.post(
        "/api/v1/messages",
        json={"channel": "webhook", "recipient": "https://hooks.example.com", "payload": {"simulate_failure": True}},
    )
    job_id = res.json()["job_id"]

    first_try = process_next_job(broker, max_retries=2)
    assert first_try is not None and first_try["status"] == "retrying"

    second_try = process_next_job(broker, max_retries=2)
    assert second_try is not None and second_try["status"] == "dead_letter"
    assert broker.stats()["dlq"] == 1

    replay = client.post("/api/v1/dlq/replay")
    assert replay.status_code == 200
    assert replay.json()["replayed"] == 1
    assert broker.stats() == {"queued": 1, "dlq": 0}

    status_res = client.get(f"/api/v1/messages/{job_id}")
    assert status_res.status_code == 200
    assert status_res.json()["status"] == "queued"
