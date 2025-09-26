import asyncio

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.models import Rooms

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels():
    return await HotelDAO.find_all()


@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int):
    return await HotelDAO.find_by_id(hotel_id)


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_hotel_id(hotel_id):
    return await RoomsDAO.get_rooms_by_hotel(hotel_id)


@router.get("/{hotels_id}/room")
async def get_room_by_hotel_id(hotel_id: int):
    return await RoomsDAO.find_by_another_id(hotel_id=hotel_id)
