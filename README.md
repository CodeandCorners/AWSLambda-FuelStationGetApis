# Lambda for querying fuel-stations fuel-prices db


Expects Body from POST event, looks up cheapest b10, closest first, as POC

```
{
    "longitude": 123
    "latitude": "123
}

```
## Inline policies that need adding to lambda
```{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "FuelFinderPrices",
			"Effect": "Allow",
			"Action": [
				"dynamodb:BatchGetItem"
			],
			"Resource": "ARN of table here"
		}
	]
}```

```{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "FuelFinderStationsStore",
			"Effect": "Allow",
			"Action": [
				"dynamodb:Query"
			],
			"Resource": [
				"ARN of table",
			    "ARN of table/index/geohash-index"
				
				]
		}
	]
}```
### Geohash dependency
EITHER

**geohash2 dependency for local testing / asserting**

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

**geohash2 dependency for lambda**
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt -t package/

pull geohash2 main folder out package and place folder in top level (same level as lambda_function.py)
delete the package folder

## Notable config
- fuelStationGeoHashPrecision = 5 # matching https://github.com/CodeandCorners/AWSLambda-FuelFinderStationStore
- GetFuelStationsService maxAmountOfFuelStationsFromDBForPerformance = 200 # No more than 200 fuel stations returned from initial search, this should never happen, we just don't want to risk pagniation in this simple POC
- limitForFuelStationsOnResponse = 20 #  No more than 20 fuel station responses returned
