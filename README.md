# Lambda for querying fuel-stations fuel-prices db


## POST /
- acceptedFuelTypes optional or provided with > 1 list elemnt

- maxAmountOfStationsToReturn optional return as many as server deems or limited to select amount. 
Example request body:
```
{
    "longitude": "123"
    "latitude": "123
    "maxAmountOfStationsToReturn": 1
    acceptedFuelTypes: ["E5", "E10"]
}

```

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
fuelStationGeoHashPrecision = 5 # matching https://github.com/CodeandCorners/AWSLambda-FuelFinderStationStore