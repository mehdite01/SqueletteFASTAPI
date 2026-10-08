from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class TestEntity:
    __test__ = False

    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime