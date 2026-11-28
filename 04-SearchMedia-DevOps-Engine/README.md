# 04-SearchMedia-DevOps-Engine

Full-stack media search, upload, and caching engine for the **OmniChain FullStack Roadmap (Module 04)**, containerized with multi-stage Docker builds and automated CI.

## Architecture & Highlights
- **Backend (`FastAPI` + `Redis` + `SQLite`):** Full-text search, pagination, secure MIME/size-validated file uploads, and Redis Cache-Aside with O(1) namespace-version invalidation (`X-Cache: HIT | MISS | BYPASS`).
- **Frontend (`React 19` + `TypeScript` + `Tailwind v4`):** React Router, TanStack Query state management, client-side upload validation, and Vitest component tests.
- **DevOps & Quality:** Multi-stage Dockerfiles (non-root Python + Nginx SPA), `docker-compose.yml` with healthchecks, `.pre-commit-config.yaml`, ADR 0001, and GitHub Actions CI.

## Quick Start (Docker Compose)

    docker compose up --build

- **Frontend:** `http://localhost:3000`
- **Backend API:** `http://localhost:8001/health`
- **Redis:** `localhost:6379`

## Architecture Decision Records
- [ADR 0001: Redis Cache-Aside Strategy & Secure Media Uploads](./docs/adr/0001-redis-cache-aside-and-media-storage.md)
