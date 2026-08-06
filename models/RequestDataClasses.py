from dataclasses import dataclass

@dataclass
class RequestParam:
    longitude: str
    latitude: str
    maxAmountOfStationsToReturn: int | None
    acceptedFuelTypes: list[str] | None

@dataclass
class RequestLocationConverted:
    geohash: str
    precision: int