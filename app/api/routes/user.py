from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.db.schemas.user import UserCreate
from app.services.user_service import user_services

router = APIRouter()

@router.post("/signup/")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    return await user_services.signup(user, db)