from models.RequestDataClasses import RequestParam
import json
import boto3
from services.GetFuelStationsService import getResponse

# DB
dynamodb = boto3.resource("dynamodb")


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
        getResponse(params, fuelStationGeoHashPrecision, dynamodb)
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
              }
