from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.test_entity import TestEntity
from app.domain.repositories.repository import Repository
from app.infrastructure.database.mappers.test_entity_mapper import (
    TestEntityMapper,
)
from app.infrastructure.database.models.entity_model import (
    TestEntity as TestEntityModel,
)
from app.infrastructure.database.repositories.sqlalchemy_repository import (
    SQLAlchemyRepository,
)


class TestEntityRepository(
    SQLAlchemyRepository[TestEntity, TestEntityModel],
    Repository[TestEntity],
):
    __test__ = False

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(
            session=session,
            model=TestEntityModel,
            mapper=TestEntityMapper(),
        )