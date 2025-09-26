from pydantic import BaseModel, json


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: str
    quantity: int
    image_id: int