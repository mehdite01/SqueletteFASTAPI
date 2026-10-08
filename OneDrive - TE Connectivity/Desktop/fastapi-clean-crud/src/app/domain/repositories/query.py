from dataclasses import dataclass, field
from typing import Generic, TypeVar

from app.domain.repositories.filter import Filter

T = TypeVar("T")


@dataclass(frozen=True)
class Sort:
    field: str
    descending: bool = False


@dataclass(frozen=True)
class Query(Generic[T]):
    page: int = 1
    page_size: int = 20
    sort: Sort | None = None
    filters: list[Filter] = field(default_factory=list)