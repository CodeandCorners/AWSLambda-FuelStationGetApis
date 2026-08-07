from dataclasses import dataclass
from decimal import Decimal
from models.FuelPricesDataClasses import FuelPrice
from models.FuelStationDataClasses import FuelStationWithDistance
from models.RequestDataClasses import FuelTypeRequest

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
    fuelPrice: FuelPrice,
    fuelType: FuelTypeRequest) -> FuelStationPriceResponse:

    station = stationWithDistance.fuelStation

    return FuelStationPriceResponse(
        id=station.id,
        nameOfStation=station.name,
        fuelTypeAndPrice=FuelTypeAndPrice(
            fuelType="E10",
            price=fuelPrice.e10Price
        ),
        longitude=station.location.longitude,
        latitude=station.location.latitude,
        distanceInMilesFromRequestLocation=stationWithDistance.distanceInMiles
    )