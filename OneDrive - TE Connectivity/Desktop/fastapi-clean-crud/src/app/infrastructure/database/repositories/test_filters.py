import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.entities.test_entity import TestEntity
from app.domain.repositories.filter import Filter, FilterOperator
from app.domain.repositories.query import Query, Sort
from app.infrastructure.database.mappers.test_entity_mapper import (
    TestEntityMapper,
)
from app.infrastructure.database.models.entity_model import (
    TestEntity,
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
            model=TestEntityModel,
            mapper=mapper,
        )

        entities = [
            TestEntity(
                id=uuid4(),
                name="Alice",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            TestEntity(
                id=uuid4(),
                name="Alicia",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            TestEntity(
                id=uuid4(),
                name="Bob",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            TestEntity(
                id=uuid4(),
                name="Charlie",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
        ]

        for entity in entities:
            await repository.add(entity)

        await session.commit()

        print("=== CONTAINS ===")

        contains_query = Query[TestEntity](
            page=1,
            page_size=100,
            sort=Sort(
                field="name",
                descending=False,
            ),
            filters=[
                Filter(
                    field="name",
                    operator=FilterOperator.CONTAINS,
                    value="ali",
                )
            ],
        )

        contains_page = await repository.list_paginated(
            contains_query
        )

        print("TOTAL:", contains_page.total)

        for entity in contains_page.items:
            print(entity.name)

        print("\n=== EQUALS ===")

        equals_query = Query[TestEntity](
            page=1,
            page_size=100,
            filters=[
                Filter(
                    field="name",
                    operator=FilterOperator.EQUALS,
                    value="Bob",
                )
            ],
        )

        equals_page = await repository.list_paginated(
            equals_query
        )

        print("TOTAL:", equals_page.total)

        for entity in equals_page.items:
            print(entity.name)

        print("\n=== IN ===")

        in_query = Query[TestEntity](
            page=1,
            page_size=100,
            sort=Sort(
                field="name",
                descending=False,
            ),
            filters=[
                Filter(
                    field="name",
                    operator=FilterOperator.IN,
                    value=[
                        "Alice",
                        "Charlie",
                    ],
                )
            ],
        )

        in_page = await repository.list_paginated(
            in_query
        )

        print("TOTAL:", in_page.total)

        for entity in in_page.items:
            print(entity.name)

        for entity in entities:
            await repository.delete(entity.id)

        await session.commit()

    await close_engine()


if __name__ == "__main__":
    asyncio.run(main())