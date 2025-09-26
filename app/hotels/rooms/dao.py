from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import async_session
from app.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms_by_hotel(cls, hotel_id: int):
        async with async_session() as session:
            res = await session.scalars(
                select(Rooms).where(Rooms.hotel_id == int(hotel_id))
            )
            return res.all()


