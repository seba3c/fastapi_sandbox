# FastAPI Sandbox

A minimal FastAPI project for experimentation and learning, using [uv](https://docs.astral.sh/uv/) for dependency management.

This project serves two purposes:

1. **Learn and experiment with FastAPI** — exploring patterns, best practices, and building small features.
2. **Learn and use OpenCode as the main AI coding tool** — all development assistance, code generation, and agent-driven workflows are done through [OpenCode](https://opencode.ai/), making it the primary AI pair-programmer for this codebase.

This project uses [autoskills.sh](https://www.autoskills.sh/) and [skills.sh](https://skills.sh/) to manage agent skills.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

## Quick Commands

| Command | Description |
|---------|-------------|
| `make run-uvicorn` | Run API with uvicorn auto-reload |
| `make run-fastapi` | Run via FastAPI CLI dev server |
| `make test` | Run tests |
| `make code-check` | Check linting and formatting (read-only) |
| `make code-fix` | Fix linting issues |
| `make code-format` | Format code |
| `make dep-sync` | Sync dependencies |
| `make pre-commit-install` | Install git hooks |
| `make pre-commit-run` | Run hooks manually |
| `make docker-run` | Start API via Docker Compose |
| `make docker-test` | Run tests in Docker |

## Run

```bash
uv run uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Test

```bash
uv run pytest -v
```

## Commands

### Dependency management

```bash
uv sync                              # Install / sync all dependencies
uv add <package>                     # Add a runtime dependency
uv add --dev <package>               # Add a dev dependency
```

### Run development server

```bash
uv run fastapi dev                   # FastAPI CLI with auto-reload
# or
uv run uvicorn app.main:app --reload # Uvicorn directly
```

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Lint & format

```bash
uv run pre-commit run --all-files    # Run all hooks on all files
uv run ruff check .                  # Lint only
uv run ruff check --fix .            # Lint with auto-fix
uv run ruff format .                 # Format only
```

### Pre-commit hooks

```bash
uv run pre-commit install            # Install git hooks (runs on every commit)
uv run pre-commit run --all-files    # Run manually across all files
```

## Project Structure

```
app/
├── main.py                    # FastAPI app factory; registers the v1 router
├── core/
│   └── config.py              # pydantic-settings Settings (reads .env via env_file)
├── api/
│   ├── dependencies.py        # Shared FastAPI dependencies (e.g., get_settings)
│   └── v1/
│       ├── router.py          # Aggregates all v1 endpoint routers
│       └── endpoints/
│           ├── __init__.py
│           ├── health.py      # GET /api/v1/health
│           └── json_tests.py # Various JSON serialization tests
├── schemas/                   # Pydantic input/output models
├── services/                  # Business logic layer
└── repositories/              # Data access layer
tests/
└── test_health.py
```

## Configuration

Settings are defined in `app/config.py` using `pydantic-settings`. Create a `.env` file to override defaults:

```env
APP_NAME="My App"
DEBUG=true
```
