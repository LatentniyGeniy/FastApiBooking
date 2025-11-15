from pydantic import BaseModel
from sqlalchemy import select, insert

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.schemas.rooms import Room, RoomAdd


class RoomsRepositories(BaseRepository):
    model = RoomsModel
    schema = Room

