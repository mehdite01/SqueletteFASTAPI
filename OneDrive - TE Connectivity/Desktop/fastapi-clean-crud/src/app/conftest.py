import pytest_asyncio

from app.infrastructure.database.session import close_engine


@pytest_asyncio.fixture(autouse=True)
async def dispose_database_engine():
    yield
    await close_engine()