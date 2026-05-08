from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import Settings

settings = Settings()

engine = create_async_engine(settings.database_url, echo=settings.debug)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
