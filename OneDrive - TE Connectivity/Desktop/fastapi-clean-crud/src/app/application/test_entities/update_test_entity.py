from datetime import datetime, timezone
from uuid import UUID

from app.application.exceptions import EntityNotFoundError
from app.domain.entities.test_entity import TestEntity
from app.domain.unit_of_work import UnitOfWork


class UpdateTestEntityUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self.unit_of_work = unit_of_work

    async def execute(
        self,
        entity_id: UUID,
        name: str,
    ) -> TestEntity:
        repository = self.unit_of_work.test_entities

        entity = await repository.get_by_id(entity_id)

        if entity is None:
            raise EntityNotFoundError(
                "TestEntity",
                entity_id,
            )

        entity.name = name
        entity.updated_at = datetime.now(timezone.utc)

        updated_entity = await repository.update(entity)

        await self.unit_of_work.commit()

        return updated_entity