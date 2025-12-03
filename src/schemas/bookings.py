from datetime import date, datetime

from pydantic import BaseModel


class BookingAdd(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int

class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class Booking(BookingAdd):
    id:int
    created_at: datetime

