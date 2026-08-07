import pygeohash
from models.RequestDataClasses import RequestLocationConverted, FuelTypeRequest
from models.FuelStationDataClasses import FuelStation, FuelStationWithDistance
from models.RequestDataClasses import RequestParam
from models.FuelStationPriceResponseDataClasses import FuelStationPriceResponse, toFuelStationPriceResponse
from decimal import Decimal
from models.FuelPricesDataClasses import FuelPrice
from utils.FuelStationHelper import sortClosestFirstAddDistance
from utils.FuelPricesHelper import findCheapest
from db.FuelPricesDB import getFuelPrices
from db.FuelStationsDB import getFuelStations

maxAmountOfFuelStationsFromDBForPerformance = 200


def convertToGeoHash(longitude: str, latitude: str, precision: int) -> RequestLocationConverted:
    converted = pygeohash.encode(
                float(latitude),
                float(longitude),
                precision=precision
            )
    return RequestLocationConverted(converted, precision)

def returnClosestGeoHashes(requestLocationConverted: RequestLocationConverted) -> list[str]:
    gh = requestLocationConverted.geohash

    top = pygeohash.get_adjacent(gh, "top")
    bottom = pygeohash.get_adjacent(gh, "bottom")
    left = pygeohash.get_adjacent(gh, "left")
    right = pygeohash.get_adjacent(gh, "right")

    return [
        top,
        bottom,
        left,
        right,
        pygeohash.get_adjacent(top, "left"),
        pygeohash.get_adjacent(top, "right"),
        pygeohash.get_adjacent(bottom, "left"),
        pygeohash.get_adjacent(bottom, "right"),
    ]
def getFuelPricesById(ids: list[str], dynamoDb) -> list[FuelPrice]:
    return getFuelPrices(ids,dynamoDb)

def getFuelStationsByGeoHashes(geoHashes: list[str], limit: int, dynamoDb) -> list[FuelStation]:
    return getFuelStations(geoHashes, limit, dynamoDb)

def getResponse(
    request: RequestParam,
    precision: int,
    maxRecordsToReturn: int,
    dynamodb
) -> list[FuelStationPriceResponse]:

    converted = convertToGeoHash(
        request.longitude,
        request.latitude,
        precision
    )
    print(f"convertedRequestToGeoHash {converted}")

    closestGeoHashes = returnClosestGeoHashes(
        converted
    )
    print(f"closestGeoHashes {closestGeoHashes}")

    stations = getFuelStationsByGeoHashes(
        closestGeoHashes,
        maxAmountOfFuelStationsFromDBForPerformance,
        dynamodb
    )
    print(f"stationsFoundByGeoHashes {len(stations)}")

    closestStations = sortClosestFirstAddDistance(
        Decimal(request.latitude),
        Decimal(request.longitude),
        stations,
    )
    print(f"closestStations {len(closestStations)}")

    stationIds: list[str] = [
        station.fuelStation.id
        for station in closestStations
    ]
    print(f"stationIds {len(stationIds)}")

    fuelPrices: list[FuelPrice] = getFuelPricesById(
        stationIds,
        dynamodb
    )
    print(f"fuelPrices found by stationids {len(fuelPrices)}")

    cheapestStations: list[tuple[FuelStationWithDistance, FuelPrice]] = findCheapest(
        closestStations,
        fuelPrices,
        request.fuelType,
        maxRecordsToReturn
    )
    print("HERE 8")
    print(f"cheapestStations {len(cheapestStations)}")
    print("HERE 9")
    return [
        toFuelStationPriceResponse(
            station,
            price,
            request.fuelType
        )
        for station, price in cheapestStations
    ]

