import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_request_id_is_returned() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200

    request_id = response.headers.get(
        "X-Request-ID",
    )

    assert request_id is not None
    assert len(request_id) > 0


@pytest.mark.asyncio
async def test_existing_request_id_is_preserved() -> None:
    transport = ASGITransport(app=app)

    request_id = "test-request-id-123"

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get(
            "/health",
            headers={
                "X-Request-ID": request_id,
            },
        )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == request_id


@pytest.mark.asyncio
async def test_process_time_header_is_returned() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200

    process_time = response.headers.get(
        "X-Process-Time-MS",
    )

    assert process_time is not None

    elapsed = float(process_time)

    assert elapsed >= 0