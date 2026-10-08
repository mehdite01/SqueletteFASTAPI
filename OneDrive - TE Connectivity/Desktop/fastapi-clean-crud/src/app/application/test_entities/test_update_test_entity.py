from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.application.test_entities.update_test_entity import (
    UpdateTestEntityUseCase,
)
from app.domain.entities.test_entity import TestEntity
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.database.unit_of_work import (
    SQLAlchemyUnitOfWork,
)


@pytest.mark.asyncio
async def test_update_test_entity() -> None:
    entity_id = uuid4()

    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            entity = TestEntity(
                id=entity_id,
                name="Before Update",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )

            await unit_of_work.test_entities.add(entity)
            await unit_of_work.commit()

    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            use_case = UpdateTestEntityUseCase(unit_of_work)

            result = await use_case.execute(
                entity_id=entity_id,
                name="After Update",
            )

            assert result.id == entity_id
            assert result.name == "After Update"

    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            stored = await unit_of_work.test_entities.get_by_id(
                entity_id
            )

            assert stored is not None
            assert stored.name == "After Update"