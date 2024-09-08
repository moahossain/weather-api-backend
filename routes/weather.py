from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from handlers.weather import get_future_5_hours_weather,get_weather_data

router = APIRouter()



@router.get("/weather/details/")
async def get_weather_details(lat: float = Query(...), lon: float = Query(...)):
    weather = await get_weather_data(lat, lon)
    
    if weather:
        # Extract current weather data
        current_weather = weather['current']
        location_name = weather['location']['name']
        current_time = weather['location']['localtime']
        current_temp = current_weather['temp_c']
        pressure = current_weather['pressure_mb']
        wind_speed = current_weather['wind_kph']
        
        # Extract forecast data for the next 3 days
        forecast_days = weather['forecast']['forecastday']  # Get today and the next 2 days
        forecast_list = []

        for day in forecast_days:
            day_forecast = {
                "date": day['date'],
                "morning_temp": day['hour'][6]['temp_c'],  # 6 AM
                "afternoon_temp": day['hour'][12]['temp_c'],  # 12 PM
                "evening_temp": day['hour'][18]['temp_c'],  # 6 PM
                "night_temp": day['hour'][21]['temp_c'],  # 9 PM
            }
            forecast_list.append(day_forecast)
        
        return {
            "location": location_name,
            "current_time": current_time,
            "current_temperature": f"{current_temp}°C",
            "pressure": f"{pressure} mb",
            "wind_speed": f"{wind_speed} kph",
            "next_3_days_forecast": forecast_list
        }
    else:
        raise HTTPException(status_code=404, detail="Weather data not found.")



@router.get("/weather/next5hours/")
async def get_weather(lat: float = Query(...), lon: float = Query(...)):
    weather = await get_future_5_hours_weather(lat,lon)
    
    if weather:
        forecast_day = weather['forecast']['forecastday'][0]
        current_hour = datetime.now().hour
        
        next_5_hours_weather = []
        for hour_data in forecast_day['hour']:
            forecast_time = datetime.strptime(hour_data['time'], '%Y-%m-%d %H:%M')
            if current_hour <= forecast_time.hour < current_hour + 5:
                temp = hour_data['temp_c']
                condition = hour_data['condition']['text']
                next_5_hours_weather.append({
                    "time": forecast_time.strftime('%I %p'),
                    "temperature": f"{temp}°C",
                    "condition": condition
                })
        
        return {"next_5_hours": next_5_hours_weather}
    else:
        raise HTTPException(status_code=404, detail="Weather data not found.")
