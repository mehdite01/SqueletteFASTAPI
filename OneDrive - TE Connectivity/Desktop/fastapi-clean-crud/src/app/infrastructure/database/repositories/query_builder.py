from typing import Any

from sqlalchemy import Select, func, select

from app.domain.repositories.query import Query
from app.infrastructure.database.repositories.filter_expression_builder import (
    FilterExpressionBuilder,
)
from app.infrastructure.database.repositories.sort_expression_builder import (
    SortExpressionBuilder,
)


class SQLAlchemyQueryBuilder:
    def __init__(
        self,
        model: type[Any],
    ) -> None:
        self.model = model

        self.filter_builder = FilterExpressionBuilder(
            model
        )

        self.sort_builder = SortExpressionBuilder(
            model
        )

    def build_count_statement(
        self,
        query: Query[Any],
    ) -> Select[Any]:
        statement = select(
            func.count()
        ).select_from(self.model)

        for filter_ in query.filters:
            expression = self.filter_builder.build(
                filter_
            )

            statement = statement.where(
                expression
            )

        return statement

    def build_data_statement(
        self,
        query: Query[Any],
    ) -> Select[Any]:
        statement = select(self.model)

        for filter_ in query.filters:
            expression = self.filter_builder.build(
                filter_
            )

            statement = statement.where(
                expression
            )

        if query.sort is not None:
            sort_expression = self.sort_builder.build(
                query.sort
            )

            statement = statement.order_by(
                sort_expression
            )
        else:
            statement = statement.order_by(
                self.model.id
            )

        offset = (query.page - 1) * query.page_size

        return (
            statement
            .offset(offset)
            .limit(query.page_size)
        )