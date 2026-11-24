.PHONY: up down lint test

up:
	docker compose up -d --wait

down:
	docker compose down

lint:
	ruff check src tests
	black --check src tests
	mypy src

test:
	pytest -v
