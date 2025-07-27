from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.db.models.user import User
from app.db.schemas.user import UserCreate, UserLogin
from app.decorators.handle_exceptions import handle_exceptions
from app.middlewares.authentication_middleware import auth
from app.services.user_service import user_services

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/sign-up/")
@handle_exceptions
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    return await user_services.signup(auth, user, db)


@router.post("/sign-in/")
@handle_exceptions
async def signin(user: UserLogin, db: Session = Depends(get_db)):
    return await user_services.signin(auth, user, db)


@router.post("/fetch-user-details/")
@handle_exceptions
async def get_user(user: User = Depends(auth.decode_access_token)):
    return await user_services.get_user(user)
