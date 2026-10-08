from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T


class ApiError(BaseModel):
    code: str
    message: str
    details: object | None = None


class ApiErrorResponse(BaseModel):
    success: bool = False
    error: ApiError


class ApiPageResponse(BaseModel, Generic[T]):
    success: bool = True
    data: list[T]
    page: int
    page_size: int
    total: int
    total_pages: int