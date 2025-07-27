from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.api.dependencies import get_db
from app.core.config import settings
from app.services.user_service import user_crud


class AuthenticationMiddleware:
    def __init__(self) -> None:
        db_gen = get_db()
        self.db = next(db_gen)

    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict, expires_delta: Optional[int] = None):
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=(expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    def decode_access_token(self, token: str = Header(...)):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            userid = payload.get("userid")
            if userid is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = user_crud.get_user_by_id(db=self.db, user_id=userid)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_password_hash(self, password):
        return self.__pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.__pwd_context.verify(plain_password, hashed_password)


auth = AuthenticationMiddleware()

# Authentication function using JWT token
# def authenticate_user(username: str, password: str):
#     user = user query
#     if not user or user["password"] != password:
#         return False
#     return user
