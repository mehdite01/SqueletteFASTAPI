from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.test_entity import TestEntity
from app.domain.repositories.repository import Repository
from app.domain.unit_of_work import UnitOfWork
from app.infrastructure.database.repositories.test_entity_repository import (
    TestEntityRepository,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

        self.test_entities: Repository[TestEntity] = (
            TestEntityRepository(session)
        )

    async def __aenter__(
        self,
    ) -> "SQLAlchemyUnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()

        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()