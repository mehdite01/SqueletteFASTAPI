from typing import Any

from sqlalchemy.sql.elements import ColumnElement

from app.domain.repositories.filter import Filter, FilterOperator
from app.infrastructure.database.repositories.model_field_resolver import (
    ModelFieldResolver,
)


class FilterExpressionBuilder:
    def __init__(
        self,
        model: type[Any],
    ) -> None:
        self.field_resolver = ModelFieldResolver(
            model
        )

    def build(
        self,
        filter_: Filter,
    ) -> ColumnElement[bool]:
        column = self.field_resolver.resolve(
            filter_.field
        )

        operator = filter_.operator
        value: Any = filter_.value

        if operator == FilterOperator.EQUALS:
            return column == value

        if operator == FilterOperator.NOT_EQUALS:
            return column != value

        if operator == FilterOperator.GREATER_THAN:
            return column > value

        if operator == FilterOperator.GREATER_THAN_OR_EQUAL:
            return column >= value

        if operator == FilterOperator.LESS_THAN:
            return column < value

        if operator == FilterOperator.LESS_THAN_OR_EQUAL:
            return column <= value

        if operator == FilterOperator.CONTAINS:
            return column.contains(value)

        if operator == FilterOperator.STARTS_WITH:
            return column.startswith(value)

        if operator == FilterOperator.ENDS_WITH:
            return column.endswith(value)

        if operator == FilterOperator.IN:
            if not isinstance(
                value,
                (list, tuple, set),
            ):
                raise ValueError(
                    "IN operator requires a list, tuple, or set"
                )

            return column.in_(value)

        raise ValueError(
            f"Unsupported filter operator: {operator}"
        )