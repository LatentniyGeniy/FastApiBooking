from src.repositories.base import BaseRepository
from src.models.users import UsersModel
from src.schemas.users import User


class UsersRepositories(BaseRepository):
    model = UsersModel
    schema = User