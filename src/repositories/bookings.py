from src.repositories.base import BaseRepository
from src.models.bookings import BookingsModel
from src.schemas.bookings import Booking


class BookingsRepositories(BaseRepository):
    model = BookingsModel
    schema = Booking
