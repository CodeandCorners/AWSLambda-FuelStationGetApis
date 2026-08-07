from models.FuelStationDataClasses import FuelStationWithDistance
from models.FuelPricesDataClasses import FuelPrice, FuelPriceFound
from models.RequestDataClasses import FuelTypeEnum

def findCheapest(
    closestStations: list[FuelStationWithDistance],
    fuelPrices: list[FuelPrice],
    fuelType: FuelTypeEnum,
    limit: int
) -> list[tuple[FuelStationWithDistance, FuelPriceFound]]:
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
            case FuelTypeEnum.E10:
                if fuelPrice and fuelPrice.e10Price is not None:
                    candidates.append(
                                     (
                                         stationWithDistance,
                                         fuelPrice.e10Price
                                     )
                                 )
            case FuelTypeEnum.E5:
                if fuelPrice and fuelPrice.e5Price is not None:
                    candidates.append(
                                            (
                                                     stationWithDistance,
                                                     FuelPriceFound(fuelPrice.id,
                                                                    FuelTypeEnum.E5,
                                                                    fuelPrice.e5Price
                                                                    )
                                            )
                                             )
            case FuelTypeEnum.B7Standard:
                if fuelPrice and fuelPrice.b7StandardPrice is not None:
                    candidates.append(
                                                 (
                                                     stationWithDistance,
                                                     FuelPriceFound(fuelPrice.id,
                                                                    FuelTypeEnum.B7Standard,
                                                                    fuelPrice.b7StandardPrice
                                                                    )
                                             )
                    )
            case FuelTypeEnum.B10:
                if fuelPrice and fuelPrice.b10Price is not None:
                    candidates.append(
                                                 (
                                                     stationWithDistance,
                                                     FuelPriceFound(fuelPrice.id,
                                                                    FuelTypeEnum.B10,
                                                                    fuelPrice.b10Price
                                                                    )
                                             )
                    )
            case FuelTypeEnum.B7Premium:
                if fuelPrice and fuelPrice.b7PremiumPrice is not None:
                    candidates.append(
                                                 (
                                                     stationWithDistance,
                                                     FuelPriceFound(fuelPrice.id,
                                                                    FuelTypeEnum.B7Premium,
                                                                    fuelPrice.b7PremiumPrice
                                                                    )
                                             )
                    )
            case FuelTypeEnum.HVO:
                if fuelPrice and fuelPrice.hvoPrice is not None:
                    candidates.append(
                                                 (
                                                     stationWithDistance,
                                                     FuelPriceFound(fuelPrice.id,
                                                                    FuelTypeEnum.HVO,
                                                                    fuelPrice.hvoPrice
                                                                    )
                                             )
                    )
                
    if not candidates:
        return []

    candidates.sort(
                        key=lambda item: (
                        item[1].fuelPrice,
                        item[0].distanceInMiles
            ))
    
    return candidates[:limit]
    