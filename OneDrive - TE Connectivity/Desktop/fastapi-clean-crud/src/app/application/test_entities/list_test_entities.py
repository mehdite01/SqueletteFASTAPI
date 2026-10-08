from app.domain.entities.test_entity import TestEntity
from app.domain.repositories.page import Page
from app.domain.repositories.query import Query
from app.domain.unit_of_work import UnitOfWork


class ListTestEntitiesUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self.unit_of_work = unit_of_work

    async def execute(
        self,
        query: Query[TestEntity],
    ) -> Page[TestEntity]:
        return await self.unit_of_work.test_entities.list_paginated(
            query
        )