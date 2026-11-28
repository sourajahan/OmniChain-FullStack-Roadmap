from fastapi import FastAPI, Header, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings, settings
from app.security import SecurityAndAuditMiddleware, SlidingWindowRateLimiter


def create_app(cfg: Settings | None = None) -> FastAPI:
    active_cfg = cfg or settings
    app = FastAPI(title="CloudShield Production Gateway", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=active_cfg.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type", "X-API-Key", "X-Request-ID"],
    )

    limiter = SlidingWindowRateLimiter(
        max_requests=active_cfg.rate_limit_requests,
        window_seconds=active_cfg.rate_limit_window_seconds,
    )
    app.add_middleware(SecurityAndAuditMiddleware, limiter=limiter)

    @app.get("/health")
    def health(response: Response) -> dict[str, str]:
        response.headers["Cache-Control"] = "no-store"
        return {"status": "ok", "env": active_cfg.app_env}

    @app.get("/api/v1/public/catalog")
    def public_catalog(response: Response) -> dict[str, object]:
        response.headers["Cache-Control"] = "public, max-age=300, stale-while-revalidate=60"
        return {
            "service": "OmniChain CloudShield Gateway",
            "cdn_cacheable": True,
            "modules": ["OmniStore", "SearchMedia", "CloudShield"],
        }

    @app.get("/api/v1/admin/audit")
    def admin_audit(x_api_key: str | None = Header(default=None)) -> dict[str, str]:
        if x_api_key != active_cfg.api_secret_key:
            raise HTTPException(status_code=401, detail="Invalid or missing API key.")
        return {"audit": "verified", "access": "granted"}

    return app


app = create_app()
