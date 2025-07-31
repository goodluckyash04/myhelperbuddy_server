from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.db.models.user import User
from app.decorators.handle_exceptions import handle_exceptions
from app.middlewares.authentication_middleware import auth
from app.services.ipo_services import ipo_services

router = APIRouter(prefix="/ipo", tags=["IPO"])


@router.get("/refresh/")
# @handle_exceptions
def refresh(
    db: Session = Depends(get_db), user: User = Depends(auth.decode_access_token)
):
    return ipo_services.refresh_ipos(db=db)


@router.get("/fetch-ipo-details/")
@handle_exceptions
async def fetch_ipos(
    status: str = Query(default="open"),
    db: Session = Depends(get_db),
    user: User = Depends(auth.decode_access_token),
):
    return await ipo_services.fetch_ipos(status, db)
