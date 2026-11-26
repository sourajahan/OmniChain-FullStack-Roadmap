from fastapi import FastAPI

app = FastAPI(
    title="CoreAuth Order API",
    version="0.1.0",
    description="Zero-Trust Auth, RBAC & Order Engine for OmniChain",
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
