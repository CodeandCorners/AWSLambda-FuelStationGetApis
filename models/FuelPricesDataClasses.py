from dataclasses import dataclass
from decimal import Decimal


@dataclass
class FuelPrice:
    id: str
    e5Price: Decimal | None
    e10Price: Decimal | None
    b7StandardPrice: Decimal | None
    b7PremiumPrice: Decimal | None
    b10Price: Decimal | None
    hvoPrice: Decimal | None
    createdAt: int
    ttl: int