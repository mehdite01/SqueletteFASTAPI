from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.unit_of_work import UnitOfWork
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.database.unit_of_work import (
    SQLAlchemyUnitOfWork,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_unit_of_work() -> AsyncGenerator[UnitOfWork, None]:
    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            yield unit_of_work