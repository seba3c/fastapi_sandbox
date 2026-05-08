from functools import lru_cache

from app.core.config import Settings
from app.repositories.categories import CategoryRepository


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_category_repository() -> CategoryRepository:
    return CategoryRepository()
