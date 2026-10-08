from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.repository import Repository
from app.infrastructure.database.mappers.base_mapper import BaseMapper

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

    async def list(self) -> list[TEntity]:
        result = await self.session.execute(
            select(self.model)
        )

        models = result.scalars().all()

        return [
            self.mapper.to_entity(model)
            for model in models
        ]

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