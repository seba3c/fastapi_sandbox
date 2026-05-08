from functools import lru_cache
from typing import Any, AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.repositories.categories import CategoryRepository


@lru_cache
def get_settings() -> Settings:
    return Settings()


async def get_db_session(
    request: Request,
) -> AsyncGenerator[Any, Any]:
    session_maker = request.app.state.session_maker
    async with session_maker() as session:
        yield session


def get_category_repository(
    session: AsyncSession = Depends(get_db_session),
) -> CategoryRepository:
    return CategoryRepository(session)
