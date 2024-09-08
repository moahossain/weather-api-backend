import os
import httpx
from fastapi import HTTPException
from decouple import config



WEATHER_API_KEY = config("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

WEATHER_BIT_API_KEY = config("WEATHER_BIT_API_KEY")  
WEATHER_BIT_BASE_URL = 'https://api.weatherbit.io/v2.0/alerts'

async def get_weather_data(lat: float, lon: float):
    params = {
        "key": WEATHER_API_KEY,
        "q": f"{lat},{lon}",
        "days": 3 
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data.")


async def get_future_5_hours_weather(lat: float, lon: float):
    params = {
        "key": WEATHER_API_KEY,
        "q": f"{lat},{lon}",
        "days": 1  
    }

    # Make the GET request asynchronously
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data.")





async def get_extreme_weather(lat, lon):
    print(WEATHER_BIT_API_KEY)
    params = {
        'key': WEATHER_BIT_API_KEY,
        'lat': lat,
        'lon': lon,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_BIT_BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        alerts = data.get('alerts', [])
        alert_result = []
        if alerts:
            for alert in alerts:
                alert_result.append({
                    "title": alert.get("title"),
                    "description": alert.get("description"),
                    "regions" : alert.get("regions"),
                    "severity": alert.get("severity")
                })
            return alert_result
        else:
            return "No extreme weather alerts for this location."
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve data")
    




