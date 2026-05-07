from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.dependencies import get_settings
from app.api.v1.router import api_router
from app.core.logging import configure_logging
from app.core.middleware import add_process_time_header, log_requests


API_V1 = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_logging(settings)
    yield


app = FastAPI(title="FastAPI Sandbox", lifespan=lifespan)
app.middleware("http")(add_process_time_header)
app.middleware("http")(log_requests)
app.include_router(api_router, prefix=API_V1)
