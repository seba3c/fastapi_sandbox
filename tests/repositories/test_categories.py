import pytest

from app.repositories.categories import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


@pytest.fixture
async def repository():
    return CategoryRepository()


@pytest.mark.anyio
async def test_list_empty(repository):
    categories = await repository.list()
    assert categories == []


@pytest.mark.anyio
async def test_create_category(repository):
    create = CategoryCreate(name="Test Category")
    category = await repository.create(create)
    assert category.name == "Test Category"
    assert category.id is not None


@pytest.mark.anyio
async def test_get_category(repository):
    create = CategoryCreate(name="Test Category")
    category = await repository.create(create)

    fetched = await repository.get(category.id)
    assert fetched is not None
    assert fetched.name == "Test Category"
    assert fetched.id == category.id


@pytest.mark.anyio
async def test_get_category_not_found(repository):
    fetched = await repository.get(1)
    assert fetched is None


@pytest.mark.anyio
async def test_update_category(repository):
    create = CategoryCreate(name="Original")
    category = await repository.create(create)

    update = CategoryUpdate(name="Updated")
    updated = await repository.update(category.id, update)
    assert updated is not None
    assert updated.name == "Updated"
    assert updated.id == category.id


@pytest.mark.anyio
async def test_update_category_not_found(repository):
    update = CategoryUpdate(name="Updated")
    result = await repository.update(1, update)
    assert result is None


@pytest.mark.anyio
async def test_delete_category(repository):
    create = CategoryCreate(name="To Delete")
    category = await repository.create(create)

    deleted = await repository.delete(category.id)
    assert deleted is True
    assert await repository.get(category.id) is None


@pytest.mark.anyio
async def test_delete_category_not_found(repository):
    deleted = await repository.delete(1)
    assert deleted is False
