from dataclasses import dataclass
from decimal import Decimal
from enum import Enum



@dataclass
class RequestLocationConverted:
    geohash: str
    precision: int

@dataclass
class FuelTypeRequest(Enum):
    E10 = "E10"
    E5 = "E5"
    B7Standard = "B7Standard"
    B7Premium = "B7Premium"
    HVO = "HVO"

@dataclass
class RequestParam:
    longitude: Decimal
    latitude: Decimal
    fuelType: FuelTypeRequest