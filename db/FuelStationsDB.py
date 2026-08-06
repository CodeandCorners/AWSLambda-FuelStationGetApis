from models.FuelStationDataClasses import FuelStation, OpeningTime, OpeningTimes, FuelStationLocation

from decimal import Decimal
from boto3.dynamodb.conditions import Key


tableName = "fuel-stations"

def getFuelStations(
    geoHashes: list[str],
    limit: int,
    dynamoDb
) -> list[FuelStation]:

    items = []

    for geoHash in geoHashes:
        response = dynamoDb.Table(tableName).query(
            IndexName="geohash-index",
            KeyConditionExpression=Key("geohash").eq(geoHash),
            Limit=limit
        )

        items.extend(response.get("Items", []))

    return [
        mapFuelStation(item)
        for item in items
    ]


def mapOpeningTime(item: dict) -> OpeningTime:
    return OpeningTime(
        open=item["open"],
        close=item["close"],
        is_24_hours=item["is_24_hours"]
    )


def mapOpeningTimes(item: dict) -> OpeningTimes:
    return OpeningTimes(
        monday=mapOpeningTime(item["monday"]),
        tuesday=mapOpeningTime(item["tuesday"]),
        wednesday=mapOpeningTime(item["wednesday"]),
        thursday=mapOpeningTime(item["thursday"]),
        friday=mapOpeningTime(item["friday"]),
        saturday=mapOpeningTime(item["saturday"]),
        sunday=mapOpeningTime(item["sunday"]),
    )


def mapFuelStation(item: dict) -> FuelStation:
    location = item["location"]

    return FuelStation(
        id=item["id"],
        name=item["name"],
        geohash=item["geohash"],
        ttl=item["ttl"],
        createdAt=item["createdAt"],
        location=FuelStationLocation(
            address_line_1=location["addressLine1"],
            postcode=location["postcode"],
            latitude=location["latitude"],
            longitude=location["longitude"],
        ),
        openingTimes=mapOpeningTimes(item["openingTimes"])
    )