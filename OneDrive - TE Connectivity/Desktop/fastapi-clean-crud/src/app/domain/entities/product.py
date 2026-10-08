from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass
class Product:
    id: UUID
    name: str
    description: str | None
    price: Decimal
    stock: int
    is_active: bool