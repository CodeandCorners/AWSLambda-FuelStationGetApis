from models.FuelStationDataClasses import FuelStationWithDistance
from models.FuelPricesDataClasses import FuelPrice
from models.RequestDataClasses import FuelTypeRequest

def findCheapestE10(
    closestStations: list[FuelStationWithDistance],
    fuelPrices: list[FuelPrice],
    fuelType: FuelTypeRequest,
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

        match fuelType:
            case FuelTypeRequest.E10:
                if fuelPrice and fuelPrice.e10Price is not None:
                    return candidates.append(
                                     (
                                         stationWithDistance,
                                         fuelPrice
                                     )
                                 )
            case FuelTypeRequest.E5:
                if fuelPrice and fuelPrice.e5Price is not None:
                    return candidates.append(
                                            (
                                                     stationWithDistance,
                                                     fuelPrice
                                                 )
                                             )
            case FuelTypeRequest.B7Standard:
                if fuelPrice and fuelPrice.b7StandardPrice is not None:
                    return candidates.append(
                                                 (
                                                     stationWithDistance,
                                                     fuelPrice
                                                 )
                                             )
            case FuelTypeRequest.B10:
                if fuelPrice and fuelPrice.b10Price is not None:
                    return candidates.append(
                                                 (
                                                     stationWithDistance,
                                                     fuelPrice
                                                 )
                                             )
            case FuelTypeRequest.B7Premium:
                if fuelPrice and fuelPrice.b7PremiumPrice is not None:
                    return candidates.append(
                                                 (
                                                     stationWithDistance,
                                                     fuelPrice
                                                 )
                                             )
            case FuelTypeRequest.HVO:
                if fuelPrice and fuelPrice.hvoPrice is not None:
                    return candidates.append(
                                                             (
                                                                 stationWithDistance,
                                                                 fuelPrice
                                                             )
                                                         )
                
    if not candidates:
        return []

    match fuelType:
        case FuelTypeRequest.E10:
            return candidates.sort(
                        key=lambda item: (
                        item[1].e10Price,
                        item[0].distanceInMiles
            ))[:limit]
        case FuelTypeRequest.E5:
            return candidates.sort(
                        key=lambda item: (
                        item[1].e5Price,
                        item[0].distanceInMiles
            ))[:limit]        
        case FuelTypeRequest.B7Standard:
            return candidates.sort(
                        key=lambda item: (
                        item[1].b7StandardPrice,
                        item[0].distanceInMiles
            ))[:limit]
        case FuelTypeRequest.B7Premium:
            return candidates.sort(
                        key=lambda item: (
                        item[1].b7PremiumPrice,
                        item[0].distanceInMiles
            ))[:limit]
        case FuelTypeRequest.B10:
            return candidates.sort(
                        key=lambda item: (
                        item[1].b10Price,
                        item[0].distanceInMiles
            ))[:limit]
        case FuelTypeRequest.HVO:
            return candidates.sort(
                        key=lambda item: (
                        item[1].hvoPrice,
                        item[0].distanceInMiles
            ))[:limit]
    