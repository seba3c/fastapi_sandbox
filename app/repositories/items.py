from uuid import UUID

from app.schemas.item import Item, ItemCreate, ItemUpdate


class InMemoryItemRepository:
    """In-memory repository for Item storage."""

    def __init__(self) -> None:
        self._items: dict[UUID, Item] = {}

    async def list(self) -> list[Item]:
        return list(self._items.values())

    async def get(self, item_id: UUID) -> Item | None:
        return self._items.get(item_id)

    async def create(self, item_create: ItemCreate) -> Item:
        item = Item.model_validate(item_create.model_dump())
        self._items[item.id] = item
        return item

    async def update(self, item_id: UUID, item_update: ItemUpdate) -> Item | None:
        existing = self._items.get(item_id)
        if not existing:
            return None
        update_data = item_update.model_dump(exclude_unset=True, exclude_none=True)
        updated = existing.model_copy(update=update_data)
        self._items[item_id] = updated
        return updated

    async def delete(self, item_id: UUID) -> bool:
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False
