from fastapi import APIRouter

from pwdlib import PasswordHash

from src.database import async_session_maker
from src.repositories.users import UsersRepositories
from src.schemas.users import UserRequestAdd, UserAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


password_hash = PasswordHash.recommended()

@router.post("/register")
async def register_user(
        user_data: UserRequestAdd,
):
    hashed_password = password_hash.hash(user_data.password)
    new_user_data = UserAdd(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        hashed_password=hashed_password
    )
    async with async_session_maker() as session:
        await UsersRepositories(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}