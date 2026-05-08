from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.db.session import AsyncSessionLocal
from app.repositories.categories import CategoryRepository


@lru_cache
def get_settings() -> Settings:
    return Settings()


async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


def get_category_repository(
    session: AsyncSession = Depends(get_db_session),
) -> CategoryRepository:
    return CategoryRepository(session)
