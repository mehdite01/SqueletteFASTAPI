from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.application.test_entities.delete_test_entity import (
    DeleteTestEntityUseCase,
)
from app.domain.entities.test_entity import TestEntity
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.database.unit_of_work import (
    SQLAlchemyUnitOfWork,
)


@pytest.mark.asyncio
async def test_delete_test_entity() -> None:
    entity_id = uuid4()

    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            entity = TestEntity(
                id=entity_id,
                name="To Delete",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )

            await unit_of_work.test_entities.add(entity)
            await unit_of_work.commit()

    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            use_case = DeleteTestEntityUseCase(unit_of_work)

            await use_case.execute(entity_id)

    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            result = await unit_of_work.test_entities.get_by_id(
                entity_id
            )

            assert result is None