import pytest
from uuid import uuid4


@pytest.mark.anyio
async def test_create_item(client):
    response = await client.post(
        "/api/v1/items", json={"name": "Test Item", "description": "Test Desc"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "Test Desc"
    assert "id" in data


@pytest.mark.anyio
async def test_create_item_validation_error(client):
    # Name too long
    response = await client.post("/api/v1/items", json={"name": "a" * 51})
    assert response.status_code == 422

    # Missing name
    response = await client.post("/api/v1/items", json={"description": "Desc"})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_list_items(client):
    await client.post("/api/v1/items", json={"name": "Item 1", "description": "Desc 1"})
    await client.post("/api/v1/items", json={"name": "Item 2", "description": "Desc 2"})

    response = await client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.anyio
async def test_get_item(client):
    create_response = await client.post(
        "/api/v1/items", json={"name": "Item 1", "description": "Desc 1"}
    )
    item_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Item 1"


@pytest.mark.anyio
async def test_get_item_not_found(client):
    response = await client.get(f"/api/v1/items/{uuid4()}")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_item(client):
    create_response = await client.post(
        "/api/v1/items", json={"name": "Original", "description": "Original Desc"}
    )
    item_id = create_response.json()["id"]

    response = await client.put(f"/api/v1/items/{item_id}", json={"name": "Updated"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"
    assert data["description"] == "Original Desc"


@pytest.mark.anyio
async def test_update_item_not_found(client):
    response = await client.put(f"/api/v1/items/{uuid4()}", json={"name": "Updated"})
    assert response.status_code == 404


@pytest.mark.anyio
async def test_delete_item(client):
    create_response = await client.post(
        "/api/v1/items", json={"name": "To Delete", "description": "Desc"}
    )
    item_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code == 204

    get_response = await client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 404


@pytest.mark.anyio
async def test_delete_item_not_found(client):
    response = await client.delete(f"/api/v1/items/{uuid4()}")
    assert response.status_code == 404
