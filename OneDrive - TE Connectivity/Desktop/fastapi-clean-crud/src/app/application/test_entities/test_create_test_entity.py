import asyncio

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


async def main() -> None:
    async with AsyncSessionLocal() as session:
        async with SQLAlchemyUnitOfWork(
            session
        ) as unit_of_work:
            use_case = CreateTestEntityUseCase(
                unit_of_work
            )

            created_entity = await use_case.execute(
                name="Application Layer Test"
            )

            print("CREATED:", created_entity.name)
            print("ID:", created_entity.id)

            await unit_of_work.test_entities.delete(
                created_entity.id
            )

            await unit_of_work.commit()

    await close_engine()


if __name__ == "__main__":
    asyncio.run(main())