from fastapi.testclient import TestClient

from app.main import create_app


def test_ai_vector_search_and_observability_headers() -> None:
    client = TestClient(create_app(region="eu-west-1"))

    res = client.get("/api/v1/search/semantic", params={"q": "elasticsearch vector search neural gpu", "top_k": 2})
    assert res.status_code == 200
    assert res.headers["X-Region"] == "eu-west-1"
    assert res.headers["traceparent"].startswith("00-")

    results = res.json()["results"]
    assert len(results) == 2
    assert results[0]["doc_id"] == "SKU-GPU-AI"


def test_distributed_saga_success_and_reverse_compensation() -> None:
    client = TestClient(create_app(region="us-east-1"))

    ok = client.post("/api/v1/sagas/orders", json={"order_id": "ORD-8001"})
    assert ok.status_code == 201
    ok_body = ok.json()
    assert ok_body["status"] == "COMPLETED"
    assert len(ok_body["completed_steps"]) == 3
    assert ok_body["compensated_steps"] == []

    failed = client.post(
        "/api/v1/sagas/orders",
        json={"order_id": "ORD-8002", "fail_at_step": "schedule_logistics"},
    )
    assert failed.status_code == 201
    fail_body = failed.json()
    assert fail_body["status"] == "COMPENSATED"
    assert fail_body["compensated_steps"] == ["compensate_authorize_payment", "compensate_reserve_inventory"]
    assert any(e["topic"] == "omnichain.saga.compensations" for e in fail_body["kafka_events"])

    metrics_res = client.get("/metrics")
    assert metrics_res.status_code == 200
    assert 'omnichain_saga_completed_total{region="us-east-1"} 1' in metrics_res.text
    assert 'omnichain_saga_compensated_total{region="us-east-1"} 1' in metrics_res.text
