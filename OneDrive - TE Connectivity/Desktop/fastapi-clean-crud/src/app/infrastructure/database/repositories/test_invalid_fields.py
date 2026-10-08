import asyncio

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

        print("=== INVALID FILTER FIELD ===")

        invalid_filter_query = Query(
            filters=[
                Filter(
                    field="does_not_exist",
                    operator=FilterOperator.EQUALS,
                    value="test",
                )
            ]
        )

        try:
            await repository.list_paginated(
                invalid_filter_query
            )
        except ValueError as exception:
            print("REJECTED:", exception)

        print("\n=== INVALID SORT FIELD ===")

        invalid_sort_query = Query(
            sort=Sort(
                field="does_not_exist",
                descending=False,
            )
        )

        try:
            await repository.list_paginated(
                invalid_sort_query
            )
        except ValueError as exception:
            print("REJECTED:", exception)

    await close_engine()


if __name__ == "__main__":
    asyncio.run(main())