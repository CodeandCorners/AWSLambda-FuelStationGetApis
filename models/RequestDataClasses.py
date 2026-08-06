from dataclasses import dataclass
from decimal import Decimal

@dataclass
class RequestParam:
    longitude: Decimal
    latitude: Decimal

@dataclass
class RequestLocationConverted:
    geohash: str
    precision: int