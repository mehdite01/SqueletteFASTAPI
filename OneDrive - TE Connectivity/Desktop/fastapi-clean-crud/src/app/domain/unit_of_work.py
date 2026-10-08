from abc import ABC, abstractmethod

from app.domain.entities.test_entity import TestEntity
from app.domain.repositories.repository import Repository


class UnitOfWork(ABC):
    test_entities: Repository[TestEntity]

    @abstractmethod
    async def __aenter__(
        self,
    ) -> "UnitOfWork":
        pass

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        pass

    @abstractmethod
    async def commit(
        self,
    ) -> None:
        pass

    @abstractmethod
    async def rollback(
        self,
    ) -> None:
        pass