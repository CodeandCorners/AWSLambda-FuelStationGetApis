from dataclasses import dataclass
from decimal import Decimal
from models.FuelPricesDataClasses import FuelPriceFound
from models.FuelStationDataClasses import FuelStationWithDistance

@dataclass
class FuelTypeAndPrice:
    fuelType: str
    price: Decimal


@dataclass
class FuelStationPriceResponse:
    # Although not strictly needed, and maps directly to GOVUK ID instead of pigeon pair db id,
    # may be useful for future API calls
    id: str
    nameOfStation: str
    fuelTypeAndPrice: FuelTypeAndPrice
    longitude: Decimal
    latitude: Decimal
    # This "could" be a separate API in an ideal world
    distanceInMilesFromRequestLocation: Decimal

# Finish this, 
def toFuelStationPriceResponse(
    stationWithDistance: FuelStationWithDistance,
    fuelPriceFound: FuelPriceFound) -> FuelStationPriceResponse:

    station = stationWithDistance.fuelStation

    return FuelStationPriceResponse(
        id=station.id,
        nameOfStation=station.name,
        fuelTypeAndPrice=FuelTypeAndPrice(
            fuelType=fuelPriceFound.fuelType.value,
            price=fuelPriceFound.fuelPrice
        ),
        longitude=station.location.longitude,
        latitude=station.location.latitude,
        distanceInMilesFromRequestLocation=stationWithDistance.distanceInMiles
    )