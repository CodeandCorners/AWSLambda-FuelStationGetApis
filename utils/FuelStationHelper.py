from models.FuelStationDataClasses import FuelStation, FuelStationWithDistance
from decimal import Decimal
from math import radians, sin, cos, sqrt, atan2

 # Calculates the straight-line distance between two latitude/longitude points.
    # I Take NO credit for this
    # Haversine formula
def calculateDistanceMiles(
    requestLatitude: Decimal,
    requestLongitude: Decimal,
    stationLatitude: Decimal,
    stationLongitude: Decimal
) -> Decimal:

    earthRadiusMiles = Decimal("3958.8")

    lat1 = radians(float(requestLatitude))
    lon1 = radians(float(requestLongitude))
    lat2 = radians(float(stationLatitude))
    lon2 = radians(float(stationLongitude))

    deltaLat = lat2 - lat1
    deltaLon = lon2 - lon1

    a = (
        sin(deltaLat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(deltaLon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return Decimal(str(earthRadiusMiles * Decimal(str(c))))


def sortAndLimitClosestStations(
    requestLatitude: Decimal,
    requestLongitude: Decimal,
    fuelStations: list[FuelStation],
    limit: int | None,
) -> list[FuelStationWithDistance]:

    # Attach the calculated distance to each station
    stationsWithDistance = [
        FuelStationWithDistance(
            fuelStation=station,
            distanceInMiles=calculateDistanceMiles(
                requestLatitude,
                requestLongitude,
                station.location.latitude,
                station.location.longitude
            )
        )
        for station in fuelStations
    ]

    # Sort closest first
    stationsWithDistance.sort(
        key=lambda station: station.distanceInMiles
    )

    # Return only the closest N stations
    if(limit is None):
        return stationsWithDistance
    else:
        return stationsWithDistance[:limit]

