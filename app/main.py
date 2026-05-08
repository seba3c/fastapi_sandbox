import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.dependencies import get_settings
from app.api.v1.router import api_router
from app.core.logging import configure_logging
from app.core.middleware import add_process_time_header, log_requests


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_logging(settings)
    logger = logging.getLogger(__name__)
    logger.info("Starting %s app...", app.title)
    logger.info(
        f"Environment: {settings.environment}, "
        f"Debug: {settings.debug}, "
        f"Version: {settings.version}"
    )
    yield
    logger.info("Shutting down %s app...", app.title)


app = FastAPI(title="FastAPI ecom", lifespan=lifespan)
app.middleware("http")(add_process_time_header)
app.middleware("http")(log_requests)
app.include_router(api_router)
