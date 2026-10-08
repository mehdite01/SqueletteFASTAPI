from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.domain.entities.test_entity import TestEntity
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.database.unit_of_work import SQLAlchemyUnitOfWork


@pytest.mark.asyncio
async def test_unit_of_work_rolls_back_on_exception() -> None:
    entity_id = uuid4()

    with pytest.raises(RuntimeError):
        async with AsyncSessionLocal() as session:
            async with SQLAlchemyUnitOfWork(session) as unit_of_work:
                entity = TestEntity(
                    id=entity_id,
                    name="Rollback Test",
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )

                await unit_of_work.test_entities.add(entity)

                raise RuntimeError("Simulated failure")

    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            saved_entity = await unit_of_work.test_entities.get_by_id(
                entity_id
            )

            assert saved_entity is None