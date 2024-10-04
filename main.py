# main.py

import keyring
import requests
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


# Set the keyring backend to PlaintextKeyring
keyring.set_keyring(keyring.backends.file.PlaintextKeyring())

# Check the current keyring backend configuration
current_backend = keyring.get_keyring()
print(f"Current keyring backend: {current_backend}")

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()


api_key="zfGW0BfGdV1m7oOMQtoeMOSQlbC4j6UE"
api_key = keyring.get_password("api_key", "agriculture")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# function to get address code from address
@app.get("/weather/stations/nearby")
def get_weather_stations_nearby(latitude: float, longitude: float, radius: int=5, offset: int=0, limit: int=5, include_closed: bool=False):
    # give address, get address code from address
    # curl -X GET "https://api.agric.wa.gov.au/v2/weather/stations/nearby?latitude=-31.963512&longitude=115.857048&radius=5&offset=0&limit=25&includeClosed=false" -H "accept: application/json"
    # https://api.agric.wa.gov.au/v2/weather/stations/nearby?api_key=zfGW0BfGdV1m7oOMQtoeMOSQlbC4j6UE&latitude=-31.963512&longitude=115.857048&radius=5&offset=0&limit=25&includeClosed=false
    # http://127.0.0.1:8000/weather/stations/nearby?latitude=-31.963512&longitude=115.857048&radius=5&offset=0&limit=25&include_closed=false
    print(f"latitude: {latitude}, longitude: {longitude}, radius: {radius}, offset: {offset}, limit: {limit}, include_closed: {include_closed}")
    include_closed = str(include_closed).lower()
    url = f"https://api.agric.wa.gov.au/v2/weather/stations/nearby?api_key={api_key}&latitude={latitude}&longitude={longitude}&radius={radius}&offset={offset}&limit={limit}&includeClosed={include_closed}"
    print(f"url={url}")
    response = requests.get(url)
    print(response.json())
    return response.json()

def get_nearest_station(latitude: float, longitude: float):
    """
     {
            "stationCode": "BG001",
            "stationName": "Kings Park",
            "latitude": -31.95887,
            "longitude": 115.83821,
            "altitude": 57,
            "model": "Unidata NRL",
            "owner": "WA Department of Primary Industries and Regional Development (DPIRD)",
            "ownerCode": "DPIRD",
            "startDate": "2014-10-31",
            "endDate": null,
            "online": true,
            "status": "open",
            "comments": null,
            "jobNumber": "N3466",
            "distance": 1.94,
            "links": [
                {
                    "rel": "self",
                    "href": "http://api.agric.wa.gov.au/v2/weather/stations/BG001"
                }
            ]
        },
    
    """
    stations = get_weather_stations_nearby(latitude, longitude)
    if stations:
        stations = stations.get("collection", [])
        if stations:
            return stations[0]

# /v2/weather/stations/{stationCode}
# /v2/weather/stations/{stationCode}

def retrieve_weather_by_station_code(station_code: str):
    """
    https://api.agric.wa.gov.au/v2/weather/stations/SP/bulletin?startDate=2015-01-01&endDate=2015-01-15&offset=0&limit=25

    https://api.agric.wa.gov.au/v2/weather/stations/SP/bulletin?startDate=2024-09-20&endDate=2024-09-28&offset=0&limit=25&api_key=zfGW0BfGdV1m7oOMQtoeMOSQlbC4j6UE
    """
    url = f"https://api.agric.wa.gov.au/v2/weather/stations/{station_code}/bulletin?startDate=2015-01-01&endDate=2015-01-15&offset=0&limit=25"
    exp_weather_dict = {
  "metadata": {
    "status": 200,
    "links": [
      {
        "href": "https://api.dpird.wa.gov.au/path/to/resource",
        "rel": "self"
      }
    ]
  },
  "data": {
    "stationCode": "SP",
    "stationName": "South Perth",
    "summaries": [
      {
        "stationCode": "SP",
        "stationName": "South Perth",
        "period": {
          "from": "2016-12-21T09:15:00.000Z",
          "to": "2016-12-21T09:30:00.000Z",
          "year": 2016,
          "month": 12,
          "day": 21,
          "hour": 9,
          "minute": 30
        },
        "airTemperature": {
          "min": 8,
          "minTime": "2024-09-21T10:38:57.297Z",
          "max": 23.7,
          "maxTime": "2024-09-21T10:38:57.297Z"
        },
        "relativeHumidity": {
          "min": 65,
          "minTime": "2024-09-21T10:38:57.297Z",
          "max": 89,
          "maxTime": "2024-09-21T10:38:57.297Z"
        },
        "soilTemperature": {
          "min": 16.5,
          "minTime": "2024-09-21T10:38:57.297Z",
          "max": 21.2,
          "maxTime": "2024-09-21T10:38:57.297Z"
        },
        "wind": [
          {
            "height": 3,
            "avg": {
              "speed": 22
            },
            "max": {
              "speed": 53.64,
              "time": "2012-12-01T07:28:03Z",
              "direction": {
                "degrees": 210,
                "compassPoint": "SW"
              }
            }
          }
        ],
        "panEvaporation": 0,
        "evapotranspiration": {
          "shortCrop": 12.2,
          "tallCrop": 14.2
        },
        "solarExposure": 26458.1,
        "rainfall": 200.3,
        "links": [
          {
            "href": "https://api.dpird.wa.gov.au/path/to/resource",
            "rel": "self"
          }
        ]
      }
    ]
  }
}
    url = ""
    weather_dict = {}
    return weather_dict

# get retrieve a listing of our weather stations with the following URL:
# https://api.agric.wa.gov.au/v2/weather/stations.json?api_key=zfGW0BfGdV1m7oOMQtoeMOSQlbC4j6UE
@app.get("/weather/stations")
def get_weather_stations():
    url = "https://api.agric.wa.gov.au/v2/weather/stations.json?api_key=zfGW0BfGdV1m7oOMQtoeMOSQlbC4j6UE"
    response = requests.get(url)
    print(response.json())
    return response.json()


# postcode
# https://github.com/deanpribetic/AustralianPostcodeSearch
# https://developers.auspost.com.au/apis/pacpcs-registration
# https://github.com/bhaveshgodhani/australianpostcodes

import httplib
import urllib
import json

connection = httplib.HTTPSConnection('auspost.com.au', 443, timeout = 30)
headers = {AUTH-KEY-GOES-HERE}
suburb = raw_input('Enter a suburb: ')
urlSuburb = urllib.quote(suburb.upper())
urlString = '/api/postcode/search.json?q=' + urlSuburb
connection.request('GET', urlString, None, headers)

try:
	response = connection.getresponse()
	content = response.read()
	resultDict = json.loads(content)
	localitiesDict = resultDict.get('localities')
	localityList = localitiesDict.get('locality')

	postcodes = ''
	if isinstance(localityList,dict):
		postcodes = localityList.get('location')+ ', ' + localityList.get('state') + ': ' + str(localityList.get('postcode'))
	else:
		for item in localityList:
			postcodes = postcodes + item.get('location')+ ', ' + item.get('state') + ': ' + str(item.get('postcode')) + '\n'
	print(postcodes.strip())	

except httplib.HTTPException, e:
	print('Exception during request')