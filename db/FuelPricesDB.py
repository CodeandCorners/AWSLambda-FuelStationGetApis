from models.FuelPricesDataClasses import FuelPrice


def getFuelPrices(
    stationIds: list[str],
    dynamodb
) -> list[FuelPrice]:

    response = dynamodb.batch_get_item(
        RequestItems={
            "fuel-prices": {
                "Keys": [
                    {
                        "id": stationId
                    }
                    for stationId in stationIds
                ]
            }
        }
    )

    items = response["Responses"].get(
        "fuel-prices",
        []
    )

    return [
        mapFuelPrice(item)
        for item in items
    ]


def mapFuelPrice(item: dict) -> FuelPrice:

    return FuelPrice(
        id=item["id"],
        e5Price=item.get("e5Price"),
        e10Price=item.get("e10Price"),
        b7StandardPrice=item.get("b7StandardPrice"),
        b7PremiumPrice=item.get("b7PremiumPrice"),
        b10Price=item.get("b10Price"),
        hvoPrice=item.get("hvoPrice"),
        createdAt=item["insertedAt"],
        ttl=item["ttl"]
    )
