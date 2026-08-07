from models.FuelStationDataClasses import FuelStationWithDistance
from models.FuelPricesDataClasses import FuelPrice
from models.RequestDataClasses import FuelTypeRequest

def findCheapest(
    closestStations: list[FuelStationWithDistance],
    fuelPrices: list[FuelPrice],
    fuelType: FuelTypeRequest,
    limit: int
) -> list[tuple[FuelStationWithDistance, FuelPrice]]:
    print("HERE 1")
    pricesById = {
        price.id: price
        for price in fuelPrices
    }

    candidates = []
    print("HERE 2")
    for stationWithDistance in closestStations:
        fuelPrice = pricesById.get(
            stationWithDistance.fuelStation.id
        )
        print("HERE 3")
        match fuelType:
            case FuelTypeRequest.E10:
                print("HERE 4")
                if fuelPrice and fuelPrice.e10Price is not None:
                    print("HERE 5")
                    candidates.append(
                                     (
                                         stationWithDistance,
                                         fuelPrice
                                     )
                                 )
            case FuelTypeRequest.E5:
                if fuelPrice and fuelPrice.e5Price is not None:
                    candidates.append(
                                            (
                                                     stationWithDistance,
                                                     fuelPrice
                                                 )
                                             )
            case FuelTypeRequest.B7Standard:
                if fuelPrice and fuelPrice.b7StandardPrice is not None:
                    candidates.append(
                                                 (
                                                     stationWithDistance,
                                                     fuelPrice
                                                 )
                                             )
            case FuelTypeRequest.B10:
                if fuelPrice and fuelPrice.b10Price is not None:
                    candidates.append(
                                                 (
                                                     stationWithDistance,
                                                     fuelPrice
                                                 )
                                             )
            case FuelTypeRequest.B7Premium:
                if fuelPrice and fuelPrice.b7PremiumPrice is not None:
                    candidates.append(
                                                 (
                                                     stationWithDistance,
                                                     fuelPrice
                                                 )
                                             )
            case FuelTypeRequest.HVO:
                if fuelPrice and fuelPrice.hvoPrice is not None:
                    candidates.append(
                                                             (
                                                                 stationWithDistance,
                                                                 fuelPrice
                                                             )
                                                         )
                
    if not candidates:
        return []
    print("HERE 6")

    match fuelType:
        case FuelTypeRequest.E10:
            print("HERE 7")
            candidates.sort(
                        key=lambda item: (
                        item[1].e10Price,
                        item[0].distanceInMiles
            ))
        case FuelTypeRequest.E5:
            candidates.sort(
                        key=lambda item: (
                        item[1].e5Price,
                        item[0].distanceInMiles
            ))      
        case FuelTypeRequest.B7Standard:
            candidates.sort(
                        key=lambda item: (
                        item[1].b7StandardPrice,
                        item[0].distanceInMiles
            ))
        case FuelTypeRequest.B7Premium:
            candidates.sort(
                        key=lambda item: (
                        item[1].b7PremiumPrice,
                        item[0].distanceInMiles
            ))
        case FuelTypeRequest.B10:
            candidates.sort(
                        key=lambda item: (
                        item[1].b10Price,
                        item[0].distanceInMiles
            ))
        case FuelTypeRequest.HVO:
            candidates.sort(
                        key=lambda item: (
                        item[1].hvoPrice,
                        item[0].distanceInMiles
            ))
    return candidates[:limit]
    