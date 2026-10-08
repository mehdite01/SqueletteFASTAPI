from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.page import Page
from app.domain.repositories.query import Query
from app.domain.repositories.repository import Repository
from app.infrastructure.database.mappers.base_mapper import BaseMapper
from app.infrastructure.database.repositories.query_builder import (
    SQLAlchemyQueryBuilder,
)

TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel")


class SQLAlchemyRepository(
    Repository[TEntity],
    Generic[TEntity, TModel],
):
    def __init__(
        self,
        session: AsyncSession,
        model: type[TModel],
        mapper: BaseMapper[TEntity, TModel],
    ) -> None:
        self.session = session
        self.model = model
        self.mapper = mapper

        self.query_builder = SQLAlchemyQueryBuilder(
            model
        )

    async def get_by_id(
        self,
        entity_id: UUID,
    ) -> TEntity | None:
        model = await self.session.get(
            self.model,
            entity_id,
        )

        if model is None:
            return None

        return self.mapper.to_entity(model)

    async def list(
        self,
    ) -> list[TEntity]:
        result = await self.session.execute(
            select(self.model)
        )

        models = result.scalars().all()

        return [
            self.mapper.to_entity(model)
            for model in models
        ]

    async def list_paginated(
        self,
        query: Query[TEntity],
    ) -> Page[TEntity]:
        if query.page < 1:
            raise ValueError(
                "page must be greater than or equal to 1"
            )

        if query.page_size < 1:
            raise ValueError(
                "page_size must be greater than or equal to 1"
            )

        count_statement = (
            self.query_builder.build_count_statement(
                query
            )
        )

        data_statement = (
            self.query_builder.build_data_statement(
                query
            )
        )

        count_result = await self.session.execute(
            count_statement
        )

        total = count_result.scalar_one()

        result = await self.session.execute(
            data_statement
        )

        models = result.scalars().all()

        entities = [
            self.mapper.to_entity(model)
            for model in models
        ]

        return Page(
            items=entities,
            total=total,
            page=query.page,
            page_size=query.page_size,
        )

    async def add(
        self,
        entity: TEntity,
    ) -> TEntity:
        model = self.mapper.to_model(entity)

        self.session.add(model)

        await self.session.flush()
        await self.session.refresh(model)

        return self.mapper.to_entity(model)

    async def update(
        self,
        entity: TEntity,
    ) -> TEntity:
        model = self.mapper.to_model(entity)

        merged_model = await self.session.merge(model)

        await self.session.flush()
        await self.session.refresh(merged_model)

        return self.mapper.to_entity(merged_model)

    async def delete(
        self,
        entity_id: UUID,
    ) -> None:
        model = await self.session.get(
            self.model,
            entity_id,
        )

        if model is not None:
            await self.session.delete(model)
            await self.session.flush()