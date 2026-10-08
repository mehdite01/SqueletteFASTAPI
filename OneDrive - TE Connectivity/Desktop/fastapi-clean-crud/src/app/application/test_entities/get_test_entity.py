from uuid import UUID

from app.domain.entities.test_entity import TestEntity
from app.domain.unit_of_work import UnitOfWork


class GetTestEntityUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self.unit_of_work = unit_of_work

    async def execute(
        self,
        entity_id: UUID,
    ) -> TestEntity | None:
        return await self.unit_of_work.test_entities.get_by_id(
            entity_id
        )