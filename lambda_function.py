from models.RequestDataClasses import RequestParam
import json
import boto3
from services.GetFuelStationsService import getCheapestB10Response
from dataclasses import asdict
from utils.JsonWritesHelper import DecimalEncoder

# DB
dynamodb = boto3.resource("dynamodb")
limitForFuelStations = 200

# Request
fuelStationGeoHashPrecision: int = 5


def getBodyParams(event) -> RequestParam | None:
    body = json.loads(event["body"])
    longitude = body.get("longitude")
    latitude = body.get("latitude")
    maxAmountOfStationsToReturn = body.get("maxAmountOfStationsToReturn")
    acceptedFuelTypes = body.get("fuelTypes", [])

    if(longitude is None or latitude is None):
        print("longitude / latitude Key not provided in body")
        return None
    elif (longitude == "" or latitude == ""):
        print("Coordinates provided but empty string")
        return None
    elif(acceptedFuelTypes == []):
        print("fuelTypes provided but empty list, either remove the field or provide a list of accepted fuels")
    else:
        return RequestParam(
            longitude = longitude,
            latitude = latitude,
            maxAmountOfStationsToReturn = maxAmountOfStationsToReturn,
            acceptedFuelTypes = acceptedFuelTypes
        )


def lambda_handler(event, context):
    params: RequestParam | None  = getBodyParams(event)
    if(params is None):
        return {
             'statusCode': 400,
            'body': json.dumps('Error With request body, look at logs')
        }
    else:
        response = getCheapestB10Response(params, fuelStationGeoHashPrecision,limitForFuelStations, dynamodb)
        return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
              },
        "body": json.dumps(
            [asdict(item) for item in response],
            cls=DecimalEncoder
            )
    }