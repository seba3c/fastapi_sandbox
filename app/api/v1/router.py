from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.v1.endpoints import json_tests

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(json_tests.router, prefix="/json", tags=["json_tests"])
