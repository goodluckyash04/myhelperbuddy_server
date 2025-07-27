from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api.error_handlers import response
from app.core.logging_config import logger
from app.db.crud.user import user_crud
from app.db.schemas.user import UserCreate, UserLogin


class UserService:
    async def signup(self, auth, data: UserCreate, db: Session):

        if user_crud.get_user_by_username(db, data.username):
            raise HTTPException(status_code=400, detail="Username already exists.")

        if user_crud.get_user_by_email(db, data.email):
            raise HTTPException(status_code=400, detail="Email already exists.")

        if data.password != data.rpassword:
            raise HTTPException(status_code=400, detail="Passwords do not match.")

        hashed_password = auth.get_password_hash(data.password)

        user_crud.create_user(
            db,
            username=data.username,
            password=hashed_password,
            name=data.name,
            email=data.email,
        )

        logger.info(f"{data.username} Created.")
        return response.success_response(
            status_code=201, message="Welcome onboard. Login to Continue"
        )

    async def signin(self, auth, data: UserLogin, db: Session):
        user = user_crud.get_user_by_username(
            db, data.userid
        ) or user_crud.get_user_by_username(db, data.userid)

        if not user or not auth.verify_password(data.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid Credential.")

        context = jsonable_encoder(user, include={"name", "username", "email"})
        context["access_token"] = auth.create_access_token(data={"userid": user.id})

        logger.info(f"User  {user.id} Logged in.")
        return response.success_response(
            status_code=200, message="Login Successful!!", data=context
        )

    async def get_user(self, user):

        context = jsonable_encoder(user, include={"name", "username", "email"})

        logger.info(f"fetched user details of {user.id}.")
        return response.success_response(
            status_code=200, message="Success!!", data=context
        )


user_services = UserService()
