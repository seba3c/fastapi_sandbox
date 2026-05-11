from __future__ import annotations

from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryBulkCreate,
    CategoryOrNone,
)
from app.schemas.common import PaginationParams


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(self) -> list[Category]:
        result = await self._session.execute(select(Category))
        return list(result.scalars().all())

    async def paginated_list(self, params: PaginationParams | None = None):
        if params is None:
            params = PaginationParams()
        return await apaginate(self._session, select(Category), params)

    async def get(self, category_id: int) -> CategoryOrNone:
        result = await self._session.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalar_one_or_none()

    async def create(self, category_create: CategoryCreate) -> Category:
        category = Category(name=category_create.name)
        self._session.add(category)
        await self._session.commit()
        await self._session.refresh(category)
        return category

    async def bulk_create(self, creates: CategoryBulkCreate) -> None:
        categories = [Category(name=c.name) for c in creates]
        self._session.add_all(categories)
        await self._session.commit()

    async def update(
        self, category_id: int, category_update: CategoryUpdate
    ) -> Category | None:
        category = await self.get(category_id)
        if not category:
            return None
        if category_update.name is not None:
            category.name = category_update.name
        await self._session.commit()
        await self._session.refresh(category)
        return category

    async def delete(self, category_id: int) -> bool:
        category = await self.get(category_id)
        if not category:
            return False
        await self._session.delete(category)
        await self._session.commit()
        return True
