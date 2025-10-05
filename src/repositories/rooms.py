from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel


class RoomsRepositories(BaseRepository):
    model = RoomsModel