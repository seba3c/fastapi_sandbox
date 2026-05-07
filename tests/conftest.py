import pytest
from httpx import AsyncClient, ASGITransport

from app.api.dependencies import get_item_repository
from app.main import app
from app.repositories.items import InMemoryItemRepository


@pytest.fixture
async def client():
    repo = InMemoryItemRepository()
    app.dependency_overrides[get_item_repository] = lambda: repo
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
