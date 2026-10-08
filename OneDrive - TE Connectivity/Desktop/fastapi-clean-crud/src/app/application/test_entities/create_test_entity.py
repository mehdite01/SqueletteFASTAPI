from datetime import datetime, timezone
from uuid import uuid4

from app.domain.entities.test_entity import TestEntity
from app.domain.repositories.repository import Repository
from app.domain.unit_of_work import UnitOfWork


class CreateTestEntityUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self.unit_of_work = unit_of_work

    async def execute(
        self,
        name: str,
    ) -> TestEntity:
        entity = TestEntity(
            id=uuid4(),
            name=name,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        repository = self.unit_of_work.test_entities

        created_entity = await repository.add(
            entity
        )

        await self.unit_of_work.commit()

        return created_entity