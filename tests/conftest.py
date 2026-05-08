import pytest
from httpx import AsyncClient, ASGITransport

from app.api.dependencies import get_category_repository
from app.main import app
from app.repositories.categories import CategoryRepository


@pytest.fixture
async def client():
    repo = CategoryRepository()
    app.dependency_overrides[get_category_repository] = lambda: repo
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
