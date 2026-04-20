# FastAPI Sandbox

A minimal FastAPI project for experimentation, using [uv](https://docs.astral.sh/uv/) for dependency management.

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
