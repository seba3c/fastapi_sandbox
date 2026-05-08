from app.schemas.category import Category, CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self) -> None:
        self._categories: dict[int, Category] = {}

    async def list(self) -> list[Category]:
        return list(self._categories.values())

    async def get(self, category_id: int) -> Category | None:
        return self._categories.get(category_id)

    async def create(self, category_create: CategoryCreate) -> Category:
        category = Category.model_validate(category_create.model_dump())
        self._categories[category.id] = category
        return category

    async def update(
        self, category_id: int, category_update: CategoryUpdate
    ) -> Category | None:
        existing = self._categories.get(category_id)
        if not existing:
            return None
        update_data = category_update.model_dump(exclude_unset=True, exclude_none=True)
        updated = existing.model_copy(update=update_data)
        self._categories[category_id] = updated
        return updated

    async def delete(self, category_id: int) -> bool:
        if category_id in self._categories:
            del self._categories[category_id]
            return True
        return False
