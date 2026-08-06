from models.RequestDataClasses import RequestParam
import json
import boto3
from services.GetFuelStationsService import getCheapestB10Response
from models.FuelStationPriceResponseDataClasses import FuelStationPriceResponse
from dataclasses import asdict
from utils.JsonWritesHelper import DecimalEncoder

# DB
dynamodb = boto3.resource("dynamodb")
limitForFuelStationsOnResponse = 20

# Request
fuelStationGeoHashPrecision: int = 5

def getBodyParams(event) -> RequestParam | None:
    body = json.loads(event["body"])
    longitude = body.get("longitude")
    latitude = body.get("latitude")
    if(longitude is None or latitude is None):
        print("longitude / latitude Key not provided in body")
        return None
    else:
        return RequestParam(
            longitude = longitude,
            latitude = latitude
        )


def lambda_handler(event, context):
    params: RequestParam | None= getBodyParams(event)
    if(params is None):
        return {
             'statusCode': 400,
            'body': json.dumps('Error With request body, look at logs')
        }
    else:
        response: list[FuelStationPriceResponse] = getCheapestB10Response(params, fuelStationGeoHashPrecision, limitForFuelStationsOnResponse, dynamodb)
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