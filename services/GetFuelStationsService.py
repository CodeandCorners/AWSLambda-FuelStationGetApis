import geohash2
from models.RequestDataClasses import RequestLocationConverted
from models.FuelStationDataClasses import FuelStation
from models.RequestDataClasses import RequestParam
from models.FuelStationPriceResponseDataClasses import FuelStationPriceResponse
from decimal import Decimal

def convertToGeoHash(longitude: str, latitude: str, precision: int) -> RequestLocationConverted:
    converted = geohash2.encode(
                float(latitude),
                float(longitude),
                precision=precision
            )
    return RequestLocationConverted(converted, precision)

def returnClosestGeoHashes(requestLocationConverted: RequestLocationConverted) -> list[str]:

def sortAndReturnClosestStationsOpen(requestLatitude: Decimal, requestLongitude: Decimal) -> list[FuelStation]:

def getFuelPricesById(ids: list[str]) -> list[]:

def getFuelStations(geoHashes: list[str]) -> list[FuelStation]:

def getResponse(request: RequestParam, precision: int, dynamodb) -> list[FuelStationPriceResponse]:
    converted: RequestLocationConverted = convertToGeoHash(request.longitude, request.latitude, precision)
    closestGeoHashesToRequest: list[str] = returnClosestGeoHashes(converted)
    getAllFuelStations: list[FuelStation] = getFuelStations(closestGeoHashesToRequest)
    idsOfFuelStationsFound = []
    fuelPricesFound = getFuelPricesById(idsOfFuelStationsFound)



