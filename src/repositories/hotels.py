from src.repositories.base import BaseRepository
from src.models.hotels import HotelsModel


class HotelsRepositories(BaseRepository):
    model = HotelsModel