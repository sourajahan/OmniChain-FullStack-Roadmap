import time
from collections.abc import Awaitable, Callable
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from coreauth.api.routes_auth import router as auth_router
from coreauth.api.routes_orders import router as orders_router
from coreauth.core.logging import logger

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="CoreAuth Order API",
    version="0.1.0",
    description="Zero-Trust Auth, RBAC & Order Engine for OmniChain",
)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)


@app.middleware("http")
async def security_and_correlation_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    correlation_id = request.headers.get("X-Request-ID") or uuid4().hex
    request.state.correlation_id = correlation_id
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    response.headers["X-Request-ID"] = correlation_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    logger.info(
        "http_request",
        extra={
            "extra_fields": {
                "correlation_id": correlation_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            }
        },
    )
    return response


def _problem_response(
    request: Request,
    status_code: int,
    title: str,
    detail: str,
) -> JSONResponse:
    correlation_id = getattr(request.state, "correlation_id", uuid4().hex)
    return JSONResponse(
        status_code=status_code,
        media_type="application/problem+json",
        content={
            "type": f"https://httpstatuses.com/{status_code}",
            "title": title,
            "status": status_code,
            "detail": detail,
            "instance": str(request.url.path),
            "correlation_id": correlation_id,
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return _problem_response(
        request=request,
        status_code=exc.status_code,
        title="HTTP Error",
        detail=str(exc.detail),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return _problem_response(
        request=request,
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        title="Validation Error",
        detail=str(exc.errors()),
    )


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return _problem_response(
        request=request,
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        title="Too Many Requests",
        detail=str(exc.detail),
    )


app.include_router(auth_router)
app.include_router(orders_router)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
