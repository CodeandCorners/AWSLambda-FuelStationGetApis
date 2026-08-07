# Lambda for querying fuel-stations fuel-prices db

-Is designed to integrate with the Lambdas https://github.com/CodeandCorners/AWSLambda-FuelFinderStationStore & https://github.com/CodeandCorners/AWSLambda-FuelFinderPriceStore to query Stations by User generated geohash. Calculate closest to request by Miles, then get price of type of fuel **E10 POC DEFAULTED FOR NOW** 

- and then return < 20 events to the user ordered cheapest  THEN closest

## Request 
- Expects body from API Gateway POST event. 
- Expected x-api-key set with configured value

AllowedFuelType Enums: "E10" "E5" "B7Standard" "B7Premium" "HVO"

- Example body:
```
{
    "longitude": 123.2
    "latitude": 123.1
	"fuelType" : "E10"
}

```
```bash
curl -X POST \
  "https://abc123.execute-api.eu-west-2.amazonaws.com/fuel-finder/cheapest-closest-fuel-by-type" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "latitude": 51.5074,
    "longitude": -0.1278,
	"fuelType" : "E10"
  }'
```
## Lambda Setup
- python 313 runtime not 315 as pygeohash has issues
- fuelFinderResultsApiKey Secret created with x-api-key

## Inline policies that need adding to lambda 


- For "fuel-prices" table created in https://github.com/CodeandCorners/AWSLambda-FuelFinderPriceStore
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

- - For "fuel-stations" table created in https://github.com/CodeandCorners/AWSLambda-FuelFinderStationStore
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
}
```
- Create inline policy for secret access
```{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "ReadFuelFinderAPISecret",
			"Effect": "Allow",
			"Action": "secretsmanager:GetSecretValue",
			"Resource": "ARN of secret here"
		}
	]
}
```

### pygeohash dependency when pushing up new changes to lambda

- Run commands
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


## Recommended HTTP API GATEWAY SETUP
- create API GATEWAY with integration to this lambda
- POST route /fuel-finder/cheapest-closest-fuel-by-type

## Notable config
- fuelStationGeoHashPrecision = 5 # matching https://github.com/CodeandCorners/AWSLambda-FuelFinderStationStore
- GetFuelStationsService maxAmountOfFuelStationsFromDBForPerformance = 200 # No more than 200 fuel stations returned from initial search, this should never happen, we just don't want to risk pagniation in this simple POC
- limitForFuelStationsOnResponse = 20 #  No more than 20 fuel station responses returned

## TODO 
- add fuel type to request, and create new methods to return closest of that fuel type rather than defaulting to E10
- Test 5 point precision, is it the correct amount for insert and query?