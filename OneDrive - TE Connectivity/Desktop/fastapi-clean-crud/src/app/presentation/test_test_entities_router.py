from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_create_test_entity() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/test-entities",
            json={
                "name": "API Entity",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["success"] is True
    assert data["data"]["name"] == "API Entity"
    assert "id" in data["data"]
    assert "created_at" in data["data"]
    assert "updated_at" in data["data"]


@pytest.mark.asyncio
async def test_get_nonexistent_test_entity() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get(
            "/test-entities/00000000-0000-0000-0000-000000000000"
        )

    assert response.status_code == 404

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "ENTITY_NOT_FOUND"


@pytest.mark.asyncio
async def test_create_and_get_test_entity() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        create_response = await client.post(
            "/test-entities",
            json={
                "name": "Integration Entity",
            },
        )

        assert create_response.status_code == 201

        created = create_response.json()

        assert created["success"] is True

        entity_id = created["data"]["id"]

        assert UUID(entity_id)

        get_response = await client.get(
            f"/test-entities/{entity_id}",
        )

        assert get_response.status_code == 200

        data = get_response.json()

        assert data["success"] is True
        assert data["data"]["id"] == entity_id
        assert data["data"]["name"] == "Integration Entity"


@pytest.mark.asyncio
async def test_update_test_entity() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        create_response = await client.post(
            "/test-entities",
            json={
                "name": "Before",
            },
        )

        assert create_response.status_code == 201

        entity_id = create_response.json()["data"]["id"]

        update_response = await client.put(
            f"/test-entities/{entity_id}",
            json={
                "name": "After",
            },
        )

        assert update_response.status_code == 200

        data = update_response.json()

        assert data["success"] is True
        assert data["data"]["id"] == entity_id
        assert data["data"]["name"] == "After"


@pytest.mark.asyncio
async def test_delete_test_entity() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        create_response = await client.post(
            "/test-entities",
            json={
                "name": "To Delete",
            },
        )

        assert create_response.status_code == 201

        entity_id = create_response.json()["data"]["id"]

        delete_response = await client.delete(
            f"/test-entities/{entity_id}",
        )

        assert delete_response.status_code == 204

        get_response = await client.get(
            f"/test-entities/{entity_id}",
        )

        assert get_response.status_code == 404

        data = get_response.json()

        assert data["success"] is False
        assert data["error"]["code"] == "ENTITY_NOT_FOUND"


@pytest.mark.asyncio
async def test_list_test_entities() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get(
            "/test-entities",
            params={
                "page": 1,
                "page_size": 10,
                "sort_field": "name",
                "descending": False,
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "data" in data
    assert "page" in data
    assert "page_size" in data
    assert "total" in data
    assert "total_pages" in data
    assert isinstance(data["data"], list)