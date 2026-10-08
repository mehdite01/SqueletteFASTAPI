import pytest

from app.application.test_entities.create_test_entity import (
    CreateTestEntityUseCase,
)
from app.infrastructure.database.session import (
    AsyncSessionLocal,
    close_engine,
)
from app.infrastructure.database.unit_of_work import (
    SQLAlchemyUnitOfWork,
)


@pytest.mark.asyncio
async def test_create_test_entity() -> None:
    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(session) as unit_of_work:
            use_case = CreateTestEntityUseCase(unit_of_work)

            created_entity = await use_case.execute(
                name="Pytest Entity",
            )

            assert created_entity.name == "Pytest Entity"
            assert created_entity.id is not None
            assert created_entity.created_at is not None
            assert created_entity.updated_at is not None

            saved_entity = await unit_of_work.test_entities.get_by_id(
                created_entity.id,
            )

            assert saved_entity is not None
            assert saved_entity.id == created_entity.id
            assert saved_entity.name == "Pytest Entity"

            await unit_of_work.test_entities.delete(
                created_entity.id,
            )

            await unit_of_work.commit()

    await close_engine()