import geohash2
from models.RequestDataClasses import RequestLocationConverted
from models.FuelStationDataClasses import FuelStation
from models.RequestDataClasses import RequestParam
from models.FuelStationPriceResponseDataClasses import FuelStationPriceResponse
from decimal import Decimal
from models.FuelPricesDataClasses import FuelPrice
from utils.FuelPricesHelper import sortClosestFirstAddDistance
from utils.FuelPricesHelper import findCheapestB10
from db.FuelPricesDB import getFuelPrices
from db.FuelStationsDB import getFuelStations



def convertToGeoHash(longitude: str, latitude: str, precision: int) -> RequestLocationConverted:
    converted = geohash2.encode(
                float(latitude),
                float(longitude),
                precision=precision
            )
    return RequestLocationConverted(converted, precision)

def returnClosestGeoHashes(requestLocationConverted: RequestLocationConverted) -> list[str]:
    return geohash2.neighbors(requestLocationConverted.geohash)


def getFuelPricesById(ids: list[str], dynamoDb) -> list[FuelPrice]:
    return getFuelPrices(ids,dynamoDb)

def getFuelStations(geoHashes: list[str], limit: int, dynamoDb) -> list[FuelStation]:
    return getFuelStations(geoHashes, limit, dynamoDb)

def getResponse(
    request: RequestParam,
    precision: int,
    stationLimitFromDbForPerformance: int,
    dynamodb
) -> list[FuelStationPriceResponse]:

    converted = convertToGeoHash(
        request.longitude,
        request.latitude,
        precision
    )

    closestGeoHashes = returnClosestGeoHashes(
        converted
    )

    stations = getFuelStations(
        closestGeoHashes,
        stationLimitFromDbForPerformance,
        dynamodb
    )

    closestStations = sortClosestFirstAddDistance(
        Decimal(request.latitude),
        Decimal(request.longitude),
        stations,
        stationLimit
    )

    stationIds = [
        station.fuelStation.id
        for station in closestStations
    ]

    fuelPrices = getFuelPricesById(
        stationIds,
        dynamodb
    )

    cheapestStations = findCheapestB10(
        closestStations,
        fuelPrices,
        resultLimit
    )

    return [
        toFuelStationPriceResponse(
            station,
            price
        )
        for station, price in cheapestStations
    ]

