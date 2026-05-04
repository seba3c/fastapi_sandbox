from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.middleware import add_process_time_header


API_V1 = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="FastAPI Sandbox", lifespan=lifespan)
app.middleware("http")(add_process_time_header)
app.include_router(api_router, prefix=API_V1)
