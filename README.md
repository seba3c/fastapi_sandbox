# FastAPI Sandbox

A minimal FastAPI project for experimentation, using [uv](https://docs.astral.sh/uv/) for dependency management.

This project uses [autoskills.sh](https://www.autoskills.sh/) and [skills.sh](https://skills.sh/) to manage agent skills.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

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
├── main.py          # FastAPI app instance and router registration
├── config.py        # Settings loaded from environment / .env
├── deps.py          # Shared FastAPI dependencies
├── api/
│   └── v1/
│       └── health.py  # GET /api/v1/health
└── models/          # Pydantic schemas
tests/
└── test_health.py
```

## Configuration

Settings are defined in `app/config.py` using `pydantic-settings`. Create a `.env` file to override defaults:

```env
APP_NAME="My App"
DEBUG=true
```
