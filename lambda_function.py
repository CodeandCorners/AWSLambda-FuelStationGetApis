from models.RequestDataClasses import RequestParam
import json
import boto3
from services.GetFuelStationsService import getCheapestE10Response
from models.FuelStationPriceResponseDataClasses import FuelStationPriceResponse
from dataclasses import asdict
from utils.JsonWritesHelper import DecimalEncoder

# DB
dynamodb = boto3.resource("dynamodb")
secrets = boto3.client("secretsmanager")
limitForFuelStationsOnResponse = 20

# Request
fuelStationGeoHashPrecision: int = 5

def getSecret() -> dict[str, str]:
    response = secrets.get_secret_value(
        SecretId="fuelFinderResultsApiKey"
    )

    return json.loads(response["SecretString"])


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
    headers = event.get("headers", {})
    apiKey = getSecret()["x-api-key"]
    if headers.get("x-api-key") != apiKey:
        return {
            "statusCode": 401,
            "body": "Unauthorized invalid api key"
            }

    method = event.get("requestContext", {}).get("http", {}).get("method")
    if(method != "POST"):
         return {
            "statusCode": 405,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "Method Not Allowed"})
        }
    
    params: RequestParam | None= getBodyParams(event)
    if(params is None):
        return {
             'statusCode': 400,
            'body': json.dumps('Error With request body, look at logs')
        }
    else:
        response: list[FuelStationPriceResponse] = getCheapestE10Response(params, fuelStationGeoHashPrecision, limitForFuelStationsOnResponse, dynamodb)
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