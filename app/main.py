import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.dependencies import get_settings
from app.api.v1.router import api_router
from app.core.logging import configure_logging
from app.core.middleware import add_process_time_header


API_V1 = "/api/v1"


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


app = FastAPI(title="FastAPI Sandbox", lifespan=lifespan)
app.middleware("http")(add_process_time_header)
app.include_router(api_router, prefix=API_V1)
