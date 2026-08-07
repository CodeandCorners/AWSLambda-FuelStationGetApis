import pygeohash
from models.RequestDataClasses import RequestLocationConverted, FuelTypeRequest
from models.FuelStationDataClasses import FuelStation
from models.RequestDataClasses import RequestParam
from models.FuelStationPriceResponseDataClasses import FuelStationPriceResponse, toFuelStationPriceResponse
from decimal import Decimal
from models.FuelPricesDataClasses import FuelPrice
from utils.FuelStationHelper import sortClosestFirstAddDistance
from utils.FuelPricesHelper import findCheapestE10
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
    match request.fuelType:
        case FuelTypeRequest.E10:
            print("User provided E10, Getting Cheapest Fuel")
            return getCheapestE10Response(request,precision,maxRecordsToReturn,dynamodb)
        case _:
            raise ValueError(f"Unsupported Fuel Type By API: {request.fuelType}")

def getCheapestE10Response(
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

    print(closestStations)
    stationIds = [
        station.fuelStation.id
        for station in closestStations
    ]
    print(f"stationIds {len(stationIds)}")

    fuelPrices = getFuelPricesById(
        stationIds,
        dynamodb
    )
    print(f"fuelPrices found by stationids {len(fuelPrices)}")
    print(fuelPrices)
    cheapestStations = findCheapestE10(
        closestStations,
        fuelPrices,
        maxRecordsToReturn
    )
    print(f"cheapestStations {len(cheapestStations)}")

    return [
        toFuelStationPriceResponse(
            station,
            price
        )
        for station, price in cheapestStations
    ]

