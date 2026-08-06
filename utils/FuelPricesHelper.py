from models.FuelStationDataClasses import FuelStationWithDistance
from models.FuelPricesDataClasses import FuelPrice

def findCheapestE10(
    closestStations: list[FuelStationWithDistance],
    fuelPrices: list[FuelPrice],
    limit: int
) -> list[tuple[FuelStationWithDistance, FuelPrice]]:

    pricesById = {
        price.id: price
        for price in fuelPrices
    }

    candidates = []

    for stationWithDistance in closestStations:
        fuelPrice = pricesById.get(
            stationWithDistance.fuelStation.id
        )

        # Ignore stations without E10
        if fuelPrice and fuelPrice.e10Price is not None:
            candidates.append(
                (
                    stationWithDistance,
                    fuelPrice
                )
            )

    if not candidates:
        return []

    # Cheapest E10 first, closest station wins if prices are equal
    candidates.sort(
        key=lambda item: (
            item[1].e10Price,
            item[0].distanceInMiles
        )
    )

    return candidates[:limit]