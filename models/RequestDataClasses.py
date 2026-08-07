from dataclasses import dataclass
from decimal import Decimal
from models.Enums import FuelTypeEnum


@dataclass
class RequestLocationConverted:
    geohash: str
    precision: int


@dataclass
class RequestParam:
    longitude: Decimal
    latitude: Decimal
    fuelType: FuelTypeEnum