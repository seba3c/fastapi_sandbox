import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from app.api.dependencies import get_settings
from app.api.v1.router import api_router
from app.core.exceptions import AppException
from app.core.logging import configure_logging
from app.core.middleware import add_process_time_header, log_requests
from app.db.session import create_async_engine_instance, create_async_session_maker


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

    engine = create_async_engine_instance(settings)
    session_maker = create_async_session_maker(engine)

    app.state.engine = engine
    app.state.session_maker = session_maker

    yield

    logger.info("Shutting down %s app...", app.title)
    await engine.dispose()


app = FastAPI(title="FastAPI ecom", lifespan=lifespan)
app.middleware("http")(add_process_time_header)
app.middleware("http")(log_requests)
app.include_router(api_router)
add_pagination(app)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
