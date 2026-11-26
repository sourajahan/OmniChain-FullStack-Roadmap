from fastapi import FastAPI

from coreauth.api.routes_auth import router as auth_router

app = FastAPI(
    title="CoreAuth Order API",
    version="0.1.0",
    description="Zero-Trust Auth, RBAC & Order Engine for OmniChain",
)

app.include_router(auth_router)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
