import pytest
from uuid import uuid4

from app.repositories.items import InMemoryItemRepository
from app.schemas.item import ItemCreate, ItemUpdate


@pytest.fixture
async def repository():
    return InMemoryItemRepository()


@pytest.mark.anyio
async def test_list_empty(repository):
    items = await repository.list()
    assert items == []


@pytest.mark.anyio
async def test_create_item(repository):
    create = ItemCreate(name="Test Item", description="Test Desc")
    item = await repository.create(create)
    assert item.name == "Test Item"
    assert item.description == "Test Desc"
    assert item.id is not None


@pytest.mark.anyio
async def test_get_item(repository):
    create = ItemCreate(name="Test Item", description="Test Desc")
    item = await repository.create(create)

    fetched = await repository.get(item.id)
    assert fetched is not None
    assert fetched.name == "Test Item"
    assert fetched.id == item.id


@pytest.mark.anyio
async def test_get_item_not_found(repository):
    fetched = await repository.get(uuid4())
    assert fetched is None


@pytest.mark.anyio
async def test_update_item(repository):
    create = ItemCreate(name="Original", description="Original Desc")
    item = await repository.create(create)

    update = ItemUpdate(name="Updated")
    updated = await repository.update(item.id, update)
    assert updated is not None
    assert updated.name == "Updated"
    assert updated.description == "Original Desc"
    assert updated.id == item.id


@pytest.mark.anyio
async def test_update_item_description_only(repository):
    create = ItemCreate(name="Original", description="Original Desc")
    item = await repository.create(create)

    update = ItemUpdate(description="New Desc")
    updated = await repository.update(item.id, update)
    assert updated is not None
    assert updated.name == "Original"
    assert updated.description == "New Desc"


@pytest.mark.anyio
async def test_update_item_not_found(repository):
    update = ItemUpdate(name="Updated")
    result = await repository.update(uuid4(), update)
    assert result is None


@pytest.mark.anyio
async def test_delete_item(repository):
    create = ItemCreate(name="To Delete", description="Desc")
    item = await repository.create(create)

    deleted = await repository.delete(item.id)
    assert deleted is True
    assert await repository.get(item.id) is None


@pytest.mark.anyio
async def test_delete_item_not_found(repository):
    deleted = await repository.delete(uuid4())
    assert deleted is False
