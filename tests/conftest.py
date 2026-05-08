import pytest
from httpx import AsyncClient, ASGITransport

from app.api.dependencies import get_category_repository
from app.main import app
from app.repositories.categories import CategoryRepository
from app.schemas.category import CategoryCreate


@pytest.fixture
async def repository():
    repo = CategoryRepository()
    app.dependency_overrides[get_category_repository] = lambda: repo
    yield repo
    app.dependency_overrides.clear()


@pytest.fixture
async def category_factory(repository):
    async def _make(name: str = "Test Category"):
        return await repository.create(CategoryCreate(name=name))

    return _make


@pytest.fixture
async def client(repository):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
