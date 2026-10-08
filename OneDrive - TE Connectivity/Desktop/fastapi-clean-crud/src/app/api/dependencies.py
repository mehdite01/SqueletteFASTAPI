from collections.abc import AsyncGenerator

from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.database.unit_of_work import SQLAlchemyUnitOfWork


async def get_unit_of_work() -> AsyncGenerator[
    SQLAlchemyUnitOfWork,
    None,
]:
    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            yield unit_of_work