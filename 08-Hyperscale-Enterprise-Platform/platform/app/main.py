import os
import time
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from app.saga import DistributedSagaOrchestrator
from app.vector_search import VectorSearchEngine


class IndexDocRequest(BaseModel):
    doc_id: str = Field(min_length=2, max_length=64)
    title: str = Field(min_length=2, max_length=120)
    category: str = Field(min_length=2, max_length=64)
    text: str = Field(min_length=3, max_length=1000)


class SagaRequest(BaseModel):
    order_id: str = Field(min_length=3, max_length=64)
    fail_at_step: str | None = Field(default=None, pattern="^(reserve_inventory|authorize_payment|schedule_logistics)$")


def create_app(region: str | None = None) -> FastAPI:
    active_region = region or os.getenv("REGION", "eu-west-1")
    search_engine = VectorSearchEngine()
    saga_engine = DistributedSagaOrchestrator()
    metrics = {"http_requests_total": 0, "saga_completed_total": 0, "saga_compensated_total": 0, "vector_queries_total": 0}

    app = FastAPI(title="OmniChain Hyperscale Platform", version="1.0.0")

    @app.middleware("http")
    async def observability_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
        start = time.perf_counter()
        traceparent = request.headers.get("traceparent") or f"00-{uuid.uuid4().hex}-{uuid.uuid4().hex[:16]}-01"
        response: Response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        metrics["http_requests_total"] += 1
        response.headers["traceparent"] = traceparent
        response.headers["X-Region"] = active_region
        response.headers["X-Response-Time-Ms"] = str(duration_ms)
        return response

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "omnichain-hyperscale-platform", "region": active_region}

    @app.get("/metrics", response_class=PlainTextResponse)
    def prometheus_metrics() -> str:
        lines = [
            "# HELP omnichain_http_requests_total Total HTTP requests handled",
            "# TYPE omnichain_http_requests_total counter",
            f'omnichain_http_requests_total{{region="{active_region}"}} {metrics["http_requests_total"]}',
            "# HELP omnichain_saga_completed_total Total completed distributed sagas",
            "# TYPE omnichain_saga_completed_total counter",
            f'omnichain_saga_completed_total{{region="{active_region}"}} {metrics["saga_completed_total"]}',
            "# HELP omnichain_saga_compensated_total Total compensated distributed sagas",
            "# TYPE omnichain_saga_compensated_total counter",
            f'omnichain_saga_compensated_total{{region="{active_region}"}} {metrics["saga_compensated_total"]}',
            "# HELP omnichain_vector_queries_total Total AI vector search queries",
            "# TYPE omnichain_vector_queries_total counter",
            f'omnichain_vector_queries_total{{region="{active_region}"}} {metrics["vector_queries_total"]}',
        ]
        return "\n".join(lines) + "\n"

    @app.post("/api/v1/search/index", status_code=201)
    def index_document(req: IndexDocRequest) -> dict[str, Any]:
        return search_engine.index_document(req.doc_id, req.title, req.category, req.text)

    @app.get("/api/v1/search/semantic")
    def semantic_search(q: str, top_k: int = 3) -> dict[str, Any]:
        metrics["vector_queries_total"] += 1
        return {"query": q, "results": search_engine.search(q, top_k=top_k)}

    @app.post("/api/v1/sagas/orders", status_code=201)
    def execute_order_saga(req: SagaRequest) -> dict[str, Any]:
        result = saga_engine.execute(order_id=req.order_id, fail_at_step=req.fail_at_step)
        if result["status"] == "COMPLETED":
            metrics["saga_completed_total"] += 1
        else:
            metrics["saga_compensated_total"] += 1
        return result

    @app.get("/api/v1/sagas/{saga_id}")
    def get_saga(saga_id: str) -> dict[str, Any]:
        record = saga_engine.get(saga_id)
        if not record:
            raise HTTPException(status_code=404, detail="Saga not found")
        return record

    return app


app = create_app()
