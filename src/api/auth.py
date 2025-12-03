from fastapi import APIRouter, HTTPException, status

from starlette.responses import Response

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd, UserAccess
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(db: DBDep, user_data: UserRequestAdd,):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        hashed_password=hashed_password
    )
    await db.users.add(new_user_data)
    await db.session.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(db: DBDep, user_data: UserAccess, response: Response):
    user = await db.users.get_user_with_hashed_password(email=user_data.email)
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


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", httponly=True)
    return {"status": "OK"}
