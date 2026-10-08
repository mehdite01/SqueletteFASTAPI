from typing import Any


class ModelFieldResolver:
    def __init__(
        self,
        model: type[Any],
    ) -> None:
        self.model = model

    def resolve(
        self,
        field: str,
    ) -> Any:
        mapper = self.model.__mapper__

        column = mapper.columns.get(field)

        if column is None:
            raise ValueError(
                f"Invalid query field: {field}"
            )

        return getattr(
            self.model,
            field,
        )