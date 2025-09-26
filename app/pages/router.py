from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels

router = APIRouter(
    prefix='/pages',
    tags=['front']
)

templates = Jinja2Templates(directory="app/templates")

@router.get('/hotels')
async def get_hotels_page(request: Request):
    hotels = await get_hotels()
    return templates.TemplateResponse(name='hotels.html', context= {"request": request, "hotels": hotels})