# ADR 0001: Redis Cache-Aside Strategy & Secure Media Uploads

## Status
Accepted

## Context
The SearchMedia engine serves paginated full-text search queries over media metadata while supporting authenticated/validated file uploads. Search queries are read-heavy and repetitive, whereas uploads and metadata mutations are write-infrequent.

## Decision
1. **Cache-Aside with Redis:**
   - Every paginated search request (`GET /api/v1/media?q=...&page=...&limit=...`) computes a deterministic cache key prefixed with a versioned namespace (`media:search:v{version}:...`).
   - On a cache miss, the service queries the data store, serializes the paginated response to Redis with a configurable TTL (`CACHE_TTL_SECONDS=60`), and returns `X-Cache: MISS`.
   - On a cache hit, Redis serves the response directly with `X-Cache: HIT`.
2. **O(1) Cache Invalidation via Namespace Versioning:**
   - Instead of expensive `KEYS *` scans on write, any upload or delete increments a single atomic Redis key (`media:cache_version`), instantly invalidating stale search pages.
   - If Redis is temporarily unavailable, the API gracefully degrades to direct queries (`X-Cache: BYPASS`) without failing user requests.
3. **Secure File Upload Validation:**
   - Strictly allowlist safe MIME types (`image/png`, `image/jpeg`, `image/webp`, `application/pdf`, `text/plain`).
   - Enforce a hard size ceiling (`MAX_UPLOAD_SIZE_MB=5`) and generate UUID-based filenames to prevent path traversal attacks.

## Consequences
- **Positive:** Sub-millisecond repeat search latency, zero `KEYS` blocking in Redis, and resilient fallback if Redis restarts.
- **Negative:** Slight memory overhead for expired keys until TTL eviction.
