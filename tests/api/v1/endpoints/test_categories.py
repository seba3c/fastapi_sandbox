import json
from unittest.mock import patch

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
async def test_create_category_triggers_background_task(client):
    with patch("app.api.v1.endpoints.categories.notify_category_created") as mock_task:
        response = await client.post(
            CATEGORIES_ADMIN_URL, json={"name": "Background Task Category"}
        )
        assert response.status_code == 201
        mock_task.assert_called_once()
        payload = mock_task.call_args[0][0]
        assert payload.name == "Background Task Category"
        assert payload.id == response.json()["id"]


@pytest.mark.anyio
async def test_create_category_duplicate(client, category_factory):
    await category_factory("Duplicate")
    response = await client.post(CATEGORIES_ADMIN_URL, json={"name": "Duplicate"})
    assert response.status_code == 409
    assert response.json()["detail"] == "Category with this name already exists."


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
    assert len(data["items"]) == 2
    assert data["total"] == 2
    assert data["limit"] == 50
    assert data["offset"] == 0


@pytest.mark.anyio
async def test_list_categories_pagination(client, category_factory):
    await category_factory("Category 1")
    await category_factory("Category 2")
    await category_factory("Category 3")

    response = await client.get(f"{CATEGORIES_PUBLIC_URL}?limit=1&offset=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 3
    assert data["limit"] == 1
    assert data["offset"] == 1
    assert data["items"][0]["name"] == "Category 2"


@pytest.mark.anyio
async def test_stream_categories(client, category_factory):
    category1 = await category_factory("Stream Category 1")
    category2 = await category_factory("Stream Category 2")

    response = await client.get(f"{CATEGORIES_PUBLIC_URL}/stream")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/jsonl")

    lines = response.text.strip().split("\n")
    assert len(lines) >= 2

    names = {json.loads(line)["name"] for line in lines}
    assert category1.name in names
    assert category2.name in names


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
    assert response.json()["detail"] == "Category not found"


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
    assert response.json()["detail"] == "Category not found"


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
    assert response.json()["detail"] == "Category not found"
