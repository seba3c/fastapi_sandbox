from fastapi import APIRouter

from app.api.v1.endpoints import health

from app.api.v1.endpoints import categories

api_router = APIRouter(prefix="/api")

api_router.include_router(health.router, prefix="/health")
api_router.include_router(categories.router, prefix="")
