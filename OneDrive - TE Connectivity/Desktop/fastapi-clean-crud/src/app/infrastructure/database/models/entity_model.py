from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.models.base_model import BaseModel


class TestEntity(BaseModel):
    __test__ = False
    __tablename__ = "test_entities"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )