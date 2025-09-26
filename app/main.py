from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import date
import time

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from redis import asyncio as aioredis
from sqladmin import Admin
import sentry_sdk

from app.admin.admin import *
from app.admin.auth import authentication_backend
from app.bookings.router import router as router_booking
from app.database import engine
from app.hotels.dao import HotelDAO
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from app.pages.router import router as pages_router
from app.users.router import router as users_router
from app.logger import logger


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost",
        encoding="utf-8",
        decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.close()

sentry_sdk.init(
    dsn="https://93be4649202eda69c16e57020c80304a@o4509892574117888.ingest.de.sentry.io/4509892575428688",
    send_default_pii=True,
)

app = FastAPI(lifespan=lifespan)
admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(HotelAdmin)
admin.add_view(BookingAdmin)
admin.add_view(RoomAdmin)


app.mount("/static", StaticFiles(directory="app/static"), "static")
app.include_router(users_router)
app.include_router(router_booking)
app.include_router(hotels_router)
app.include_router(pages_router)
app.include_router(images_router)

class SHotel(BaseModel):
    address : str
    name : str
    stars : int




@app.get("/hotels/{hotel_id}")
async def get_hotel_by_id(hotel_id : int, date_from, date_to):
    return hotel_id, date_from, date_to

class SchemaBooking(BaseModel):
    room_id : int
    data_from : date
    data_to : date

@app.post("/booking")
async def add_booking(booking: SchemaBooking):
    pass

@app.get('/redis_hotel')
@cache(expire=60)
async def get_some_hotel():
    return await HotelDAO.find_all()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("Request execution time", extra={
        "process time" : round(process_time, 3)
    })
    return response
