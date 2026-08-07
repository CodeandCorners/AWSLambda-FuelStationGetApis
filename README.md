# Lambda for querying fuel-stations fuel-prices db


Expects Body from POST event, looks up cheapest e10, closest first, as POC

```
{
    "longitude": 123.2
    "latitude": "123.1
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

**pygeohash dependency for lambda**
`python3 -m venv .venv`

`source .venv/bin/activate`

`pip install pygeohash==3.3.1 \
  --platform manylinux2014_x86_64 \
  --python-version 311 \
  --implementation cp \
  --only-binary=:all: \
  -t package/`

- pull pygeohash main folder out package and place folder in top level (same level as lambda_function.py)
- delete the package folder

##Lambda Setup
-python 313 runtime not 315 as pygeohash has issues

## Notable config
- fuelStationGeoHashPrecision = 5 # matching https://github.com/CodeandCorners/AWSLambda-FuelFinderStationStore
- GetFuelStationsService maxAmountOfFuelStationsFromDBForPerformance = 200 # No more than 200 fuel stations returned from initial search, this should never happen, we just don't want to risk pagniation in this simple POC
- limitForFuelStationsOnResponse = 20 #  No more than 20 fuel station responses returned
