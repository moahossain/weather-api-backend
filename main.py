import logging
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles


log = logging.getLogger("uvicorn")

from routes import weather, extreme, roads, ev_locator


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup event
#     log.info("Starting up....")
#     init_db(app)

#     yield  # Control goes to the request handling here

#     # Shutdown event
#     log.info("Shutting down...")


def create_application(life_span=None) -> FastAPI:
    _app = FastAPI(title="Weather Service", version="1.0.0")
    _app.mount("/static", StaticFiles(directory="static"), name="static")
    _app.include_router(weather.router, prefix="/api/v1", tags=["weather"])
    _app.include_router(extreme.router, prefix="/api/v1", tags=["extreme"])
    _app.include_router(roads.router, prefix="/api/v1", tags=["roads"])
    _app.include_router(ev_locator.router, prefix="/api/v1", tags=["ev-locators"])
    return _app


app = create_application()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8010)
