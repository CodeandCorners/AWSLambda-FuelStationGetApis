

def getFuelPrices(ids: list[str], dynamodb) -> None:
    dynamodb.Table("fuel-prices")