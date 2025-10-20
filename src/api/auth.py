

from fastapi import APIRouter, HTTPException, status


from starlette.responses import Response


from src.database import async_session_maker
from src.repositories.users import UsersRepositories
from src.schemas.users import UserRequestAdd, UserAdd, UserAccess
from src.services.ayth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])




@router.post("/register")
async def register_user(user_data: UserRequestAdd,):
    hashed_password = AuthService().hash_password(user_data.password)
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

@router.post("/login")
async def login_user( user_data: UserAccess, response: Response):
    async with async_session_maker() as session:
        user = await UsersRepositories(session).get_user_with_hashed_password(email=user_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="пользователь с таким email не авторизирован"
            )
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный пароль"
            )
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}