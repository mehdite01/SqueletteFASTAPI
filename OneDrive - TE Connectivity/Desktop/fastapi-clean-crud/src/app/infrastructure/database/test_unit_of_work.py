import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.entities.test_entity import TestEntity
from app.infrastructure.database.session import (
    AsyncSessionLocal,
    close_engine,
)
from app.infrastructure.database.unit_of_work import (
    SQLAlchemyUnitOfWork,
)


async def main() -> None:
    entity = TestEntity(
        id=uuid4(),
        name="UnitOfWork test",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(
            session
        ) as uow:

            await uow.test_entities.add(entity)

            await uow.commit()

            saved = await uow.test_entities.get_by_id(
                entity.id
            )

            print("SAVED:", saved.name if saved else None)

            await uow.test_entities.delete(
                entity.id
            )

            await uow.commit()

    await close_engine()


if __name__ == "__main__":
    asyncio.run(main())