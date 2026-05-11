from fastapi import APIRouter, FastAPI

from app.api.v1.endpoints import health

from app.api.v1.endpoints import categories


def register_routers(app: FastAPI) -> None:
    api_router = APIRouter(prefix="/api")

    api_router.include_router(health.router, prefix="/health")

    api_router.include_router(categories.router, prefix="")

    app.include_router(api_router)
