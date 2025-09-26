from datetime import date

from fastapi import APIRouter, Depends, Request
from pydantic.v1 import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.tasks.tasks import send_info_email
from app.users.dependencies import get_current_user
from app.users.model import Users

router = APIRouter(prefix="/booking", tags=["Booking room or hotel"])


@router.get("")
async def get_booking(
    request: Request, user: Users = Depends(get_current_user)
):  # -> list[SBooking]:
    # return await BookingDAO.find_all()
    # print(request.cookies)
    # print(request.url)
    # print(request.client)
    return user


@router.get("{booking_id}")
async def get_booking_by_id(booking_id: int):
    return await BookingDAO.find_by_id(booking_id)


@router.post("/bookings")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(
        user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to
    )
    if not booking:
        return {"error": "Booking was not created"}

    booking_dict = SBooking.model_validate(booking).model_dump()

    send_info_email.delay(user.email, booking_dict)

    return booking_dict
