# 02-CoreAuth-Order-API

Zero-Trust Authentication, Role-Based Access Control (RBAC), and Order Management API built with **FastAPI**, **SQLAlchemy 2.x**, **Alembic**, and **PostgreSQL 16**.

## Architecture (6-Layer Modular Design)
- `api/`: FastAPI routers, Pydantic v2 schemas, JWT/RBAC dependencies, RFC 7807 error handlers, and correlation-ID middleware.
- `service/`: Business logic, token rotation & replay attack detection, and order status state machine.
- `repository/`: Data-access layer with `selectinload` eager loading to prevent N+1 queries.
- `infra/`: SQLAlchemy 2.x ORM models (3NF) and database session management.
- `domain/`: Pure domain exceptions decoupled from HTTP transport.
- `core/`: Settings (`pydantic-settings`), Argon2id & PyJWT security primitives, and structured JSON logging.

## Key Security & Engineering Features
- **Argon2id** password hashing (`pwdlib`) + **JWT** short-lived access tokens.
- **Refresh Token Rotation & Replay Detection**: Reusing a revoked refresh token automatically revokes the entire token family.
- **RBAC & IDOR Protection**: Strict role enforcement (`admin`, `warehouse`, `customer`) and ownership checks on orders.
- **RFC 7807 Problem Details**: Standardized error responses with `correlation_id` (`X-Request-ID`).
- **Zero N+1 Queries**: Proven via SQLAlchemy cursor-event integration tests.

## Quick Start
```bash
cp .env.example .env
chmod 600 .env
make up
make migrate
make lint
make test
make run
```
