import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.entities.test_entity import TestEntity
from app.domain.repositories.query import Query, Sort
from app.infrastructure.database.mappers.test_entity_mapper import (
    TestEntityMapper,
)
from app.infrastructure.database.repositories.sqlalchemy_repository import (
    SQLAlchemyRepository,
)
from app.infrastructure.database.session import (
    AsyncSessionLocal,
    close_engine,
)


async def main() -> None:
    mapper = TestEntityMapper()

    async with AsyncSessionLocal() as session:
        repository = SQLAlchemyRepository(
            session=session,
            model=__import__(
                "app.infrastructure.database.models.test_entity",
                fromlist=["TestEntity"],
            ).TestEntity,
            mapper=mapper,
        )

        entities = [
            TestEntity(
                id=uuid4(),
                name="Charlie",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            TestEntity(
                id=uuid4(),
                name="Alice",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            TestEntity(
                id=uuid4(),
                name="Bob",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
        ]

        for entity in entities:
            await repository.add(entity)

        await session.commit()

        ascending_query = Query[TestEntity](
            page=1,
            page_size=100,
            sort=Sort(
                field="name",
                descending=False,
            ),
        )

        ascending_page = await repository.list_paginated(
            ascending_query
        )

        print("ASC:")
        for entity in ascending_page.items:
            print(entity.name)

        descending_query = Query[TestEntity](
            page=1,
            page_size=100,
            sort=Sort(
                field="name",
                descending=True,
            ),
        )

        descending_page = await repository.list_paginated(
            descending_query
        )

        print("\nDESC:")
        for entity in descending_page.items:
            print(entity.name)

        for entity in entities:
            await repository.delete(entity.id)

        await session.commit()

    await close_engine()


if __name__ == "__main__":
    asyncio.run(main())