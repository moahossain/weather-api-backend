from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from decouple import config

router = APIRouter()


templates = Jinja2Templates(directory="templates")


@router.get("/ev-stations/", response_class=HTMLResponse)
async def ev_stations(
    request: Request, lat: float = Query(...), lon: float = Query(...)
):
    TOM_TOM_API_KEY = config("TOM_TOM_API_KEY")
    return templates.TemplateResponse(
        request=request,
        name="ev-stations.html",
        context={"lat": lat, "lon": lon, "api_key": TOM_TOM_API_KEY},
    )
