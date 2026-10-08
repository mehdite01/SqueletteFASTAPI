from uuid import UUID

from app.application.exceptions import EntityNotFoundError
from app.domain.unit_of_work import UnitOfWork


class DeleteTestEntityUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self.unit_of_work = unit_of_work

    async def execute(
        self,
        entity_id: UUID,
    ) -> None:
        repository = self.unit_of_work.test_entities

        entity = await repository.get_by_id(entity_id)

        if entity is None:
            raise EntityNotFoundError(
                "TestEntity",
                entity_id,
            )

        await repository.delete(entity_id)

        await self.unit_of_work.commit()