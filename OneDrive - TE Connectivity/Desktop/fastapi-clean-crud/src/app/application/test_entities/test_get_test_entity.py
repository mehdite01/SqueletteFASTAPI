from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.application.test_entities.get_test_entity import (
    GetTestEntityUseCase,
)
from app.domain.entities.test_entity import TestEntity
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.database.unit_of_work import SQLAlchemyUnitOfWork


@pytest.mark.asyncio
async def test_get_test_entity_returns_existing_entity() -> None:
    entity = TestEntity(
        id=uuid4(),
        name="GET Test Entity",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            await unit_of_work.test_entities.add(entity)
            await unit_of_work.commit()

            use_case = GetTestEntityUseCase(unit_of_work)

            result = await use_case.execute(entity.id)

            assert result is not None
            assert result.id == entity.id
            assert result.name == "GET Test Entity"

            await unit_of_work.test_entities.delete(entity.id)
            await unit_of_work.commit()


@pytest.mark.asyncio
async def test_get_test_entity_returns_none_when_entity_does_not_exist() -> None:
    entity_id = uuid4()

    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            use_case = GetTestEntityUseCase(unit_of_work)

            result = await use_case.execute(entity_id)

            assert result is None