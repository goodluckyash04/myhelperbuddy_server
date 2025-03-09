from fastapi import HTTPException, status, Header
from typing import Optional
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.core.config import settings

# SECRET_KEY =  node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"  or openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY


class AuthenticationMiddleware:

    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()

        # set expiry delta
        expires_delta_time = expires_delta
        if expires_delta:
            expires_delta_time = settings.ACCESS_TOKEN_EXPIRE_MINUTES

        expire = datetime.now(timezone.utc) + expires_delta_time

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm='HS256')
        return encoded_jwt

    def decode_access_token(token: str = Header(...)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("username")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = "user_object"
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return user

    def get_password_hash(self, password):
        return self.__pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.__pwd_context.verify(plain_password, hashed_password)

auth=AuthenticationMiddleware()

# Authentication function using JWT token
# def authenticate_user(username: str, password: str):
#     user = user query
#     if not user or user["password"] != password:
#         return False
#     return user
