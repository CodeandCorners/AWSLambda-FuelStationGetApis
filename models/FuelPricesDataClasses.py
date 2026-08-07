from dataclasses import dataclass
from decimal import Decimal
from models.Enums import FuelTypeEnum


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


@dataclass
class FuelPriceFound:
    id: str
    fuelType: FuelTypeEnum
    fuelPrice: Decimal