from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.application.test_entities.list_test_entities import (
    ListTestEntitiesUseCase,
)
from app.domain.entities.test_entity import TestEntity
from app.domain.repositories.query import Query, Sort
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.database.unit_of_work import (
    SQLAlchemyUnitOfWork,
)


@pytest.mark.asyncio
async def test_list_test_entities_with_pagination() -> None:
    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            for index in range(5):
                entity = TestEntity(
                    id=uuid4(),
                    name=f"Entity {index}",
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )

                await unit_of_work.test_entities.add(entity)

            await unit_of_work.commit()

    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            use_case = ListTestEntitiesUseCase(unit_of_work)

            query = Query(
                page=1,
                page_size=2,
                sort=Sort(
                    field="name",
                    descending=False,
                ),
            )

            result = await use_case.execute(query)

            assert result.page == 1
            assert result.page_size == 2
            assert result.total >= 5
            assert len(result.items) == 2
            assert result.total_pages >= 3