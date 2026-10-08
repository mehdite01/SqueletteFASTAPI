from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from app.domain.repositories.page import Page
from app.domain.repositories.query import Query

T = TypeVar("T")


class Repository(Generic[T], ABC):

    @abstractmethod
    async def get_by_id(
        self,
        entity_id: UUID,
    ) -> T | None:
        pass

    @abstractmethod
    async def list(
        self,
    ) -> list[T]:
        pass

    @abstractmethod
    async def list_paginated(
        self,
        query: Query[T],
    ) -> Page[T]:
        pass

    @abstractmethod
    async def add(
        self,
        entity: T,
    ) -> T:
        pass

    @abstractmethod
    async def update(
        self,
        entity: T,
    ) -> T:
        pass

    @abstractmethod
    async def delete(
        self,
        entity_id: UUID,
    ) -> None:
        pass