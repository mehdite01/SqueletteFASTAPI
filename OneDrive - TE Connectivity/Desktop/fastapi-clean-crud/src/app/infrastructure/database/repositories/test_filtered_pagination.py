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
                name="Alpha",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            TestEntity(
                id=uuid4(),
                name="Albatross",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            TestEntity(
                id=uuid4(),
                name="Alpine",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            TestEntity(
                id=uuid4(),
                name="Almond",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            TestEntity(
                id=uuid4(),
                name="Alaska",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            TestEntity(
                id=uuid4(),
                name="Beta",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            TestEntity(
                id=uuid4(),
                name="Gamma",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
        ]

        for entity in entities:
            await repository.add(entity)

        await session.commit()

        filters = [
            Filter(
                field="name",
                operator=FilterOperator.STARTS_WITH,
                value="Al",
            )
        ]

        print("=== FILTERED PAGINATION ===")

        page_1 = await repository.list_paginated(
            Query[TestEntity](
                page=1,
                page_size=2,
                sort=Sort(
                    field="name",
                    descending=False,
                ),
                filters=filters,
            )
        )

        print("\nPAGE 1")
        print("ITEMS:", len(page_1.items))
        print("TOTAL:", page_1.total)
        print("TOTAL PAGES:", page_1.total_pages)

        for entity in page_1.items:
            print(entity.name)

        page_2 = await repository.list_paginated(
            Query[TestEntity](
                page=2,
                page_size=2,
                sort=Sort(
                    field="name",
                    descending=False,
                ),
                filters=filters,
            )
        )

        print("\nPAGE 2")
        print("ITEMS:", len(page_2.items))
        print("TOTAL:", page_2.total)
        print("TOTAL PAGES:", page_2.total_pages)

        for entity in page_2.items:
            print(entity.name)

        page_3 = await repository.list_paginated(
            Query[TestEntity](
                page=3,
                page_size=2,
                sort=Sort(
                    field="name",
                    descending=False,
                ),
                filters=filters,
            )
        )

        print("\nPAGE 3")
        print("ITEMS:", len(page_3.items))
        print("TOTAL:", page_3.total)
        print("TOTAL PAGES:", page_3.total_pages)

        for entity in page_3.items:
            print(entity.name)

        page_4 = await repository.list_paginated(
            Query[TestEntity](
                page=4,
                page_size=2,
                sort=Sort(
                    field="name",
                    descending=False,
                ),
                filters=filters,
            )
        )

        print("\nPAGE 4 - BEYOND RESULTS")
        print("ITEMS:", len(page_4.items))
        print("TOTAL:", page_4.total)
        print("TOTAL PAGES:", page_4.total_pages)

        for entity in page_4.items:
            print(entity.name)

        for entity in entities:
            await repository.delete(entity.id)

        await session.commit()

    await close_engine()


if __name__ == "__main__":
    asyncio.run(main())