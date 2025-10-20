from datetime import timezone, datetime, timedelta

from fastapi import APIRouter, HTTPException, status

from pwdlib import PasswordHash
import jwt
from starlette.responses import Response

from src.database import async_session_maker
from src.repositories.users import UsersRepositories
from src.schemas.users import UserRequestAdd, UserAdd, UserAccess

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


password_hash = PasswordHash.recommended()

@router.post("/register")
async def register_user(user_data: UserRequestAdd,):
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

@router.post("/login")
async def login_user( user_data: UserAccess, response: Response):
    async with async_session_maker() as session:
        user = await UsersRepositories(session).get_user_with_hashed_password(email=user_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="пользователь с таким email не авторизирован"
            )
        if not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный пароль"
            )
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}