from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    username: str
    first_name: str
    last_name: str

class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    username:str
    first_name: str
    last_name: str

class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
