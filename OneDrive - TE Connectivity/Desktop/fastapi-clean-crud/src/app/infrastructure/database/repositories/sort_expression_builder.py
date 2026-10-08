from typing import Any

from app.domain.repositories.query import Sort
from app.infrastructure.database.repositories.model_field_resolver import (
    ModelFieldResolver,
)


class SortExpressionBuilder:
    def __init__(
        self,
        model: type[Any],
    ) -> None:
        self.field_resolver = ModelFieldResolver(
            model
        )

    def build(
        self,
        sort: Sort,
    ) -> Any:
        column = self.field_resolver.resolve(
            sort.field
        )

        if sort.descending:
            return column.desc()

        return column.asc()