from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="FastAPI Sandbox", lifespan=lifespan)

app.include_router(health.router, prefix="/api/v1")
