from datetime import datetime

from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import *
from app.users.dao import UserDAO


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise HTTPException(status_code=401)
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise InvalidTokenException

    expire = payload.get("exp")
    if not expire or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id = payload.get("sub")
    if not user_id:
        raise UserIdDoesNotExitsException
    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserDoesNotExitsException
    return user
