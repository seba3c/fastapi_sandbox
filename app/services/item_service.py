from uuid import UUID

from app.repositories.items import InMemoryItemRepository
from app.schemas.item import Item, ItemCreate, ItemUpdate


class ItemService:
    """Business logic layer for Item operations."""

    def __init__(self, repository: InMemoryItemRepository) -> None:
        self.repository = repository

    async def list_items(self) -> list[Item]:
        return await self.repository.list()

    async def get_item(self, item_id: UUID) -> Item | None:
        return await self.repository.get(item_id)

    async def create_item(self, item_create: ItemCreate) -> Item:
        return await self.repository.create(item_create)

    async def update_item(self, item_id: UUID, item_update: ItemUpdate) -> Item | None:
        return await self.repository.update(item_id, item_update)

    async def delete_item(self, item_id: UUID) -> bool:
        return await self.repository.delete(item_id)
