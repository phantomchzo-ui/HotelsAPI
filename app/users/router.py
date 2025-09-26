from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_cache.decorator import cache

from app.exceptions import *
from app.tasks.tasks import send_info_email
from app.users.auth import auth_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.model import Users
from app.users.schemas import SUserRegister

router = APIRouter(
    prefix='/auth',
    tags=['Auth and Users']
)

@router.post('/register')
async def register_user(user_data: SUserRegister):
    existing_user = await UserDAO.find_one_or_none(email= user_data.email)
    if existing_user :
        raise UserAlreadyExitsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)

@router.post('/login')
async def login_user(user_data: SUserRegister, response: Response):
    user = await auth_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token",access_token, httponly=True)
    return access_token


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('booking_access_token')

@router.get('/current_user')
async def current_user(user: Users = Depends(get_current_user)):
    return user

@router.get('/users')
@cache(expire=60)
async def get_users():
    email_to = 'Phantomchzo@gmail.com'
    send_info_email.delay(email_to)
    return await UserDAO.find_all()
