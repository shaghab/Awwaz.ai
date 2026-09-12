# Awwaz developer tasks. `make help` lists them.
SHELL := /bin/bash
BACKEND := backend
FRONTEND := frontend
UV := cd $(BACKEND) && uv run
PNPM := cd $(FRONTEND) && pnpm

.DEFAULT_GOAL := help
.PHONY: help install db dev dev-backend dev-frontend migrate seed reset check check-backend check-frontend test test-backend test-frontend fmt

help: ## Show this help
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

install: ## Install backend and frontend dependencies
	cd $(BACKEND) && uv sync
	cd $(FRONTEND) && pnpm install

# --wait blocks on the compose healthcheck; without it `migrate` can race a
# still-starting server on a cold machine.
db: ## Start PostgreSQL and wait for it to accept connections
	docker compose up -d --wait postgres

dev: db migrate seed ## Start Postgres, then run both apps (Ctrl-C stops both)
	@trap 'kill 0' EXIT INT TERM; \
	$(MAKE) dev-backend & \
	$(MAKE) dev-frontend & \
	wait

dev-backend: ## Run the API with reload
	$(UV) uvicorn app.main:app --reload --port 8000

dev-frontend: ## Run the Next.js dev server
	$(PNPM) dev

migrate: ## Apply database migrations
	$(UV) alembic upgrade head

seed: ## Seed demo data (idempotent)
	$(UV) python -m app.seed

reset: ## Drop the schema and rebuild it from migrations, then seed
	$(UV) alembic downgrade base
	$(MAKE) migrate seed

check: check-backend check-frontend ## Lint, typecheck, test, and build everything

check-backend: ## ruff + mypy + pytest
	$(UV) ruff check .
	$(UV) ruff format --check .
	$(UV) mypy app
	$(UV) pytest -q

check-frontend: ## eslint + tsc + vitest + next build
	$(PNPM) lint
	$(PNPM) typecheck
	$(PNPM) test
	$(PNPM) build

test: test-backend test-frontend ## Run both test suites

test-backend:
	$(UV) pytest -q

test-frontend:
	$(PNPM) test

fmt: ## Format the backend
	$(UV) ruff format .
	$(UV) ruff check . --fix
