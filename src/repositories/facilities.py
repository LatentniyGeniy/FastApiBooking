from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesModel
from src.schemas.facilities import Facility


class FacilitiesRepositories(BaseRepository):
    model = FacilitiesModel
    schema = Facility
