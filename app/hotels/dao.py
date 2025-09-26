from app.dao.base import BaseDAO
from app.hotels.models import Hotels


class HotelDAO(BaseDAO):
    model = Hotels
