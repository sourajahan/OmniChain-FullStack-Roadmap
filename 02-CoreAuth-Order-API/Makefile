.PHONY: up down migrate lint test run

up:
	docker compose up -d

down:
	docker compose down

migrate:
	alembic upgrade head

lint:
	ruff check src tests
	mypy src

test:
	pytest -v

run:
	uvicorn coreauth.api.main:app --reload --port 8000
