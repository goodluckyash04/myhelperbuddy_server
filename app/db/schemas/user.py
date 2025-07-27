from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    rpassword: str


class UserLogin(BaseModel):
    userid: str
    password: str
