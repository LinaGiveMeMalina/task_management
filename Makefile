-include .env
export

run:
	uvicorn task_management.app:app --host 0.0.0.0 --port 8000 --reload

up:
	docker compose up -d --build

down:
	docker compose down

dev.install:
	@poetry install --no-root

db.migrate:
	alembic upgrade head

db.downgrade:
	alembic downgrade -1

lint:
	ruff check .
	mypy .

test:
	pytest -s

