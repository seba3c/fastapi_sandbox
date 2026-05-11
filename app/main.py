import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api.dependencies import get_settings
from app.api.v1.router import register_routers
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import register_middleware
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


def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI ecom", lifespan=lifespan)
    register_middleware(app)
    register_routers(app)
    add_pagination(app)
    register_exception_handlers(app)
    return app


app = create_app()
