from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import health
from app.api.v1 import json_tests


API_V1 = "/api/v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="FastAPI Sandbox", lifespan=lifespan)

app.include_router(health.router, prefix=API_V1)
app.include_router(json_tests.router, prefix=API_V1 + "/json")