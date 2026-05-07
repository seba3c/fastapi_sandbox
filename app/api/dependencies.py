from functools import lru_cache

from app.core.config import Settings
from app.repositories.items import InMemoryItemRepository


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_item_repository() -> InMemoryItemRepository:
    return InMemoryItemRepository()
