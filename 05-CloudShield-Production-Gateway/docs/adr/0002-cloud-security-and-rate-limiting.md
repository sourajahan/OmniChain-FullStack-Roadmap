# ADR 0002: Cloud Security Hardening, Rate Limiting & Secrets Strategy

## Status
Accepted

## Context
Exposing full-stack services to the public internet requires defense-in-depth aligned with OWASP Top 10: automated TLS/HTTPS, strict security headers, abuse protection, structured audit logs, zero hardcoded secrets, and automated database backups.

## Decision
1. **OWASP Top 10 Middleware:** Enforce `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, and `Referrer-Policy` on all responses.
2. **Rate Limiting:** Apply per-client sliding-window rate limiting returning standard `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `429 Too Many Requests` with `Retry-After`.
3. **Secrets Management:** Load all credentials exclusively from environment variables; reject startup in production if `API_SECRET_KEY` is missing or uses a default placeholder.
4. **HTTPS, CDN & Backups:** Terminate TLS via Caddy with automatic Let's Encrypt certificates, apply `Cache-Control` headers for CDN edge caching, and schedule compressed `pg_dump` / SQLite backups via `scripts/backup_db.sh`.

## Consequences
- **Positive:** Production-grade security posture ready for Render, Railway, or AWS deployment.
- **Negative:** Strict CSP and CORS policies require explicit allowlisting when adding new frontend origins.
