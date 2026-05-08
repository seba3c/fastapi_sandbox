import pytest

CATEGORIES_PUBLIC_URL = "/api/public/categories"
CATEGORIES_ADMIN_URL = "/api/admin/categories"


@pytest.mark.anyio
async def test_create_category(client):
    response = await client.post(CATEGORIES_ADMIN_URL, json={"name": "Test Category"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Category"
    assert "id" in data


@pytest.mark.anyio
async def test_create_category_validation_error(client):
    # Name too long
    response = await client.post(CATEGORIES_ADMIN_URL, json={"name": "a" * 51})
    assert response.status_code == 422

    # Missing name
    response = await client.post(CATEGORIES_ADMIN_URL, json={})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_list_categories(client, category_factory):
    await category_factory("Category 1")
    await category_factory("Category 2")

    response = await client.get(CATEGORIES_PUBLIC_URL)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.anyio
async def test_get_category(client, category_factory):
    category = await category_factory("Category 1")

    response = await client.get(f"{CATEGORIES_ADMIN_URL}/{category.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Category 1"


@pytest.mark.anyio
async def test_get_category_not_found(client):
    response = await client.get(f"{CATEGORIES_ADMIN_URL}/1")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_category(client, category_factory):
    category = await category_factory("Original")

    response = await client.put(
        f"{CATEGORIES_ADMIN_URL}/{category.id}", json={"name": "Updated"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"


@pytest.mark.anyio
async def test_update_category_not_found(client):
    response = await client.put(
        f"{CATEGORIES_ADMIN_URL}/99999", json={"name": "Updated"}
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_delete_category(client, category_factory):
    category = await category_factory("To Delete")

    response = await client.delete(f"{CATEGORIES_ADMIN_URL}/{category.id}")
    assert response.status_code == 204

    get_response = await client.get(f"{CATEGORIES_ADMIN_URL}/{category.id}")
    assert get_response.status_code == 404


@pytest.mark.anyio
async def test_delete_category_not_found(client):
    response = await client.delete(f"{CATEGORIES_ADMIN_URL}/1")
    assert response.status_code == 404
