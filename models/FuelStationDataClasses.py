from dataclasses import dataclass
from decimal import Decimal

@dataclass
class FuelStationLocation:
    address_line_1: str
    postcode: str
    latitude: Decimal
    longitude: Decimal

@dataclass
class OpeningTime:
    open: str
    close: str
    is_24_hours: bool

@dataclass
class OpeningTimes:
    monday: OpeningTime
    tuesday: OpeningTime
    wednesday: OpeningTime
    thursday: OpeningTime
    friday: OpeningTime
    saturday: OpeningTime
    sunday: OpeningTime


@dataclass
class FuelStation:
    id: str
    name: str
    location: FuelStationLocation
    geohash: str
    openingTimes: OpeningTimes
    ttl: int
    createdAt: int


@dataclass
class FuelStationWithDistance:
    fuelStation: FuelStation
    distanceInMiles: Decimal