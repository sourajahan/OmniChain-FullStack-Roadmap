import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, Query, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.cache import CacheService
from app.config import settings
from app.store import MediaRepository

ALLOWED_MIME_TYPES = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
    "application/pdf": ".pdf",
    "text/plain": ".txt",
}


def create_app(
    repo: MediaRepository | None = None,
    cache: CacheService | None = None,
    upload_dir: str | None = None,
) -> FastAPI:
    app = FastAPI(title="SearchMedia DevOps Engine", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    media_repo = repo or MediaRepository(settings.database_path)
    cache_service = cache or CacheService(settings.redis_url, settings.cache_ttl_seconds)
    uploads_path = Path(upload_dir or settings.upload_dir)
    uploads_path.mkdir(parents=True, exist_ok=True)

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "redis": "connected" if cache_service.ping() else "degraded",
        }

    @app.get("/api/v1/media")
    def list_media(
        response: Response,
        q: str = Query(default="", max_length=100),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, ge=1, le=50),
    ) -> dict[str, Any]:
        version = cache_service.get_version()
        if version is not None:
            cache_key = cache_service.build_search_key(version, q, page, limit)
            cached = cache_service.get_json(cache_key)
            if cached is not None:
                response.headers["X-Cache"] = "HIT"
                return cached

            result = media_repo.search(q=q, page=page, limit=limit)
            cache_service.set_json(cache_key, result)
            response.headers["X-Cache"] = "MISS"
            return result

        response.headers["X-Cache"] = "BYPASS"
        return media_repo.search(q=q, page=page, limit=limit)

    @app.post("/api/v1/media/upload", status_code=201)
    async def upload_media(
        title: str = Form(..., min_length=2, max_length=120),
        tags: str = Form(default=""),
        file: UploadFile = File(...),
    ) -> dict[str, Any]:
        content_type = file.content_type or ""
        if content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported media type: {content_type}. Allowed: {sorted(ALLOWED_MIME_TYPES)}",
            )

        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file cannot be empty.")
        if len(content) > settings.max_upload_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds maximum size of {settings.max_upload_size_mb}MB.",
            )

        media_id = str(uuid.uuid4())
        ext = ALLOWED_MIME_TYPES[content_type]
        stored_filename = f"{media_id}{ext}"
        (uploads_path / stored_filename).write_bytes(content)

        item = media_repo.create(
            media_id=media_id,
            title=title.strip(),
            tags=tags.strip(),
            original_filename=file.filename or stored_filename,
            stored_filename=stored_filename,
            content_type=content_type,
            size_bytes=len(content),
        )
        cache_service.bump_version()
        return item

    @app.delete("/api/v1/media/{media_id}", status_code=204)
    def delete_media(media_id: str) -> Response:
        stored_filename = media_repo.delete(media_id)
        if not stored_filename:
            raise HTTPException(status_code=404, detail="Media item not found.")

        file_path = uploads_path / stored_filename
        if file_path.exists():
            file_path.unlink()

        cache_service.bump_version()
        return Response(status_code=204)

    return app


app = create_app()
