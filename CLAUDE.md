# FastAPI Sandbox — Claude Context

## Commands

```bash
uv sync                                      # install / sync dependencies
uv run uvicorn app.main:app --reload         # start dev server
uv run pytest -v                             # run tests
uv add <package>                             # add a runtime dependency
uv add --dev <package>                       # add a dev dependency
```

## Architecture

- **`app/main.py`** — creates the `FastAPI` app, wires up lifespan, includes routers
- **`app/config.py`** — `Settings` class (pydantic-settings); reads `.env` and env vars
- **`app/deps.py`** — `get_settings()` FastAPI dependency (cached via `lru_cache`)
- **`app/api/v1/`** — versioned routers; register each in `app/main.py` with `app.include_router`
- **`app/models/`** — Pydantic request/response schemas

## Adding a New Endpoint

1. Create `app/api/v1/<feature>.py` with an `APIRouter`
2. Register it in `app/main.py`: `app.include_router(feature.router, prefix="/api/v1")`
3. Add a test in `tests/test_<feature>.py` using the `AsyncClient` + `ASGITransport` pattern from `tests/test_health.py`

## Testing

Tests use `httpx.AsyncClient` with `ASGITransport` (no live server needed) and `pytest-anyio` for async support. Tests run against both asyncio and trio backends automatically.

## Dependencies

- **Runtime**: `fastapi[standard]`, `pydantic-settings`
- **Dev**: `pytest`, `anyio[trio]`, `httpx`
