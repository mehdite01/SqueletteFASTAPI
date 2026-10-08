from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel")


class BaseMapper(Generic[TEntity, TModel], ABC):

    @abstractmethod
    def to_model(self, entity: TEntity) -> TModel:
        ...

    @abstractmethod
    def to_entity(self, model: TModel) -> TEntity:
        ...