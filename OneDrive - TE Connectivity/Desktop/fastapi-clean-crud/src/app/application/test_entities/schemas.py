from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateTestEntityRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )


class UpdateTestEntityRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )


class TestEntityResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime


class TestEntityPageResponse(BaseModel):
    items: list[TestEntityResponse]
    total: int
    page: int
    page_size: int
    total_pages: int