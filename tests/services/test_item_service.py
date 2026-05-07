from unittest.mock import AsyncMock

import pytest
from uuid import uuid4

from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services.item_service import ItemService


@pytest.fixture
def service():
    mock_repo = AsyncMock()
    return ItemService(repository=mock_repo)


@pytest.mark.anyio
async def test_list_items(service):
    mock_items = [Item(id=uuid4(), name="Item 1", description="Desc 1")]
    service.repository.list.return_value = mock_items
    result = await service.list_items()
    assert result == mock_items
    service.repository.list.assert_awaited_once()


@pytest.mark.anyio
async def test_get_item(service):
    item_id = uuid4()
    mock_item = Item(id=item_id, name="Item 1", description="Desc 1")
    service.repository.get.return_value = mock_item
    result = await service.get_item(item_id)
    assert result == mock_item
    service.repository.get.assert_awaited_once_with(item_id)


@pytest.mark.anyio
async def test_get_item_not_found(service):
    item_id = uuid4()
    service.repository.get.return_value = None
    result = await service.get_item(item_id)
    assert result is None


@pytest.mark.anyio
async def test_create_item(service):
    create_data = ItemCreate(name="New Item", description="New Desc")
    mock_item = Item(id=uuid4(), name="New Item", description="New Desc")
    service.repository.create.return_value = mock_item
    result = await service.create_item(create_data)
    assert result == mock_item
    service.repository.create.assert_awaited_once_with(create_data)


@pytest.mark.anyio
async def test_update_item(service):
    item_id = uuid4()
    update_data = ItemUpdate(name="Updated")
    mock_item = Item(id=item_id, name="Updated", description="Old Desc")
    service.repository.update.return_value = mock_item
    result = await service.update_item(item_id, update_data)
    assert result == mock_item
    service.repository.update.assert_awaited_once_with(item_id, update_data)


@pytest.mark.anyio
async def test_delete_item(service):
    item_id = uuid4()
    service.repository.delete.return_value = True
    result = await service.delete_item(item_id)
    assert result is True
    service.repository.delete.assert_awaited_once_with(item_id)
