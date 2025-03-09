from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.error_handlers import response
from app.db.schemas.user import UserCreate
from app.db.crud.user import user_crud
from app.core.logging_config import logger
from app.middlewares.authentication_middleware import auth


class UserService:
    async def signup(self, data: UserCreate, db: Session):
        try:
            if user_crud.get_user_by_username(db, data.username):
                raise HTTPException(status_code=400, detail="Username already exists.")

            if user_crud.get_user_by_email(db, data.email):
                raise HTTPException(status_code=400, detail="Email already exists.")

            if data.password != data.rpassword:
                raise HTTPException(status_code=400, detail="Passwords do not match.")

            hashed_password = auth.get_password_hash(data.password)

            user_crud.create_user(db,
                                  username=data.username, password=hashed_password, name=data.name, email=data.email)

            logger.info(f"{data.username} Created.")
            return response.success_response(status_code=201, message="Welcome onboard. Login to Continue")

        except HTTPException as e:
            logger.error(e.detail)
            return response.error_response(status_code=e.status_code, message=e.detail)
        except Exception as e:
            logger.critical(e)
            return response.internal_server_error()


user_services = UserService()
