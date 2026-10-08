from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class FilterOperator(StrEnum):
    EQUALS = "eq"
    NOT_EQUALS = "neq"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    IN = "in"


@dataclass(frozen=True)
class Filter:
    field: str
    operator: FilterOperator
    value: Any