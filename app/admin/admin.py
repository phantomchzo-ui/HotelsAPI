from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.model import Users


class UserAdmin(ModelView, model=Users):
    name = "User"
    name_plural = 'Users'
    column_list = [Users.id, Users.email]
    can_delete = False
    page_size = 10


class HotelAdmin(ModelView, model=Hotels):
    name = 'Hotel'
    name_plural = "Hotels"
    column_list = [Hotels.name, Hotels.location]

class BookingAdmin(ModelView, model=Bookings):
    name = 'Booking'
    name_plural = 'Bookings'
    column_list = [c.name for c in Bookings.__table__.c]

class RoomAdmin(ModelView, model=Rooms):
    name = 'Room'
    name_plural = 'Rooms'
    column_list = [c.name for c in Rooms.__table__.c]
