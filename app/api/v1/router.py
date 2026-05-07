from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.v1.endpoints import json_tests
from app.api.v1.endpoints import items

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router, prefix="/health")
api_router.include_router(json_tests.router, prefix="/json")
api_router.include_router(items.router, prefix="/items")
