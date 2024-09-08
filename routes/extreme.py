
from fastapi import APIRouter, HTTPException, Query

from handlers.weather import get_extreme_weather

router = APIRouter()




@router.get("/weather/extreme/")
async def weather_alerts(lat: float, lon: float):
    try:
        alerts = await get_extreme_weather(lat, lon)
        return {"latitude": lat, "longitude": lon, "alerts": alerts}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
