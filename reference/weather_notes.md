# weather notes

## 1. Free weather data/service/api

https://github.com/open-meteo/open-meteo

### free api

https://open-meteo.com/

### data
https://github.com/open-meteo/open-data

- download history data for a location

Get data for individual coordinates 
`curl "http://127.0.0.1:8080/v1/archive?latitude=47.1&longitude=8.4&hourly=temperature_2m&start_date=20220101&end_date=20231031"`

### service

run ur own weather api
https://github.com/open-meteo/open-data/tree/main/tutorial_weather_api

Installing the Open-Meteo Docker image 
`docker pull ghcr.io/open-meteo/open-meteo`
Download archived ERA5 data for temperature from AWS
`docker run open-meteo sync copernicus_era5_land temperature_2m --past-days 730 `(roughly 8 GB)
Launch your local API endpoint `docker run -p 8080:8080 open-meteo serve`

### sdk

- go cli
https://github.com/Rayrsn/Weather-Cli

- python sdk
https://github.com/m0rp43us/openmeteopy/blob/main/readme/ECMWF.md

## 2. Geo coding data and service

https://github.com/open-meteo/geocoding-api/blob/main/README.md
