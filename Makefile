.PHONY: run-uvicorn run-fastapi test code-check code-fix code-format dep-sync pre-commit-install pre-commit-run docker-run docker-test

# Run the FastAPI app with auto-reload (uvicorn --reload)
run-uvicorn:
	uv run uvicorn app.main:app --reload

# Run via FastAPI CLI dev server (supports auto-reload and type checking)
run-fastapi:
	uv run fastapi dev

# Run all tests with verbose output
test:
	uv run pytest -v

# Check for linting issues and verify code formatting (read-only)
code-check:
	uv run ruff check .
	uv run ruff format --check .

# Auto-fix linting issues (does not modify formatting)
code-fix:
	uv run ruff check --fix .

# Auto-format code (indentation, line breaks, etc.)
code-format:
	uv run ruff format .

# Sync dependencies from pyproject.toml
dep-sync:
	uv sync

# Install pre-commit git hooks (runs automatically on commit after this)
pre-commit-install:
	uv run pre-commit install

# Run all pre-commit hooks on all files (lint, format, yaml, whitespace, etc.)
pre-commit-run:
	uv run pre-commit run --all-files

# Build and start the API container via Docker Compose
docker-run:
	docker compose up api --build

# Run tests inside a Docker container
docker-test:
	docker compose run test
