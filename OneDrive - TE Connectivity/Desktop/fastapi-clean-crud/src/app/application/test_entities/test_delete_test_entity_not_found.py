from uuid import uuid4

import pytest

from app.application.exceptions import EntityNotFoundError
from app.application.test_entities.delete_test_entity import (
    DeleteTestEntityUseCase,
)
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.database.unit_of_work import (
    SQLAlchemyUnitOfWork,
)


@pytest.mark.asyncio
async def test_delete_test_entity_raises_when_not_found() -> None:
    entity_id = uuid4()

    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            use_case = DeleteTestEntityUseCase(unit_of_work)

            with pytest.raises(EntityNotFoundError):
                await use_case.execute(entity_id)