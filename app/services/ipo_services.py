from datetime import datetime, time

from bs4 import BeautifulSoup
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from app.api.error_handlers import response
from app.core.logging_config import logger
from app.db.models.ipo import IPO
from app.db.models.user import User
from app.services.scrapers.fetch_chittorgarh_ipos import (
    fetch_and_store_ipos,
    fetch_ipo_gmp_detail,
)


class IPOService:
    def refresh_ipos(self, db: Session):
        if fetch_and_store_ipos(db):
            return response.success_response(status_code=200)
        return response.error_response(
            status_code=500,
            message="Error while refreshing!!! please try again after sometime",
        )

    async def fetch_ipos(self, status: str, db: Session):
        now = datetime.now()
        today_date = now.date()
        today_430pm = datetime.combine(today_date, time(16, 30))
        if status.lower() == "active":
            active_ipos = (
                db.query(IPO)
                .filter(
                    func.date(IPO.opening_date) <= today_date,
                    or_(
                        func.date(IPO.closing_date)
                        > today_date,  # still open in future
                        and_(
                            func.date(IPO.closing_date) == today_date,
                            now < today_430pm,  # only show before 4:30 PM
                        ),
                    ),
                )
                .all()
            )

            for ipo in active_ipos:
                gmp_data = fetch_ipo_gmp_detail(ipo.gmp_id)
                if gmp_data:

                    ipo.ipoGmpData = jsonable_encoder(
                        gmp_data["ipoGmpData"][0],
                        include={
                            "gmp_date",
                            "gmp",
                            "subject_to_sauda",
                            "estimated_listing_price",
                            "gmp_percent_calc",
                            "up_down_status",
                            "sub2",
                            "est_profit",
                            "last_updated_gmp",
                            "max_ipo_price",
                        },
                    )
                    ipo.ipoGmpData["gmp_percent_calc"] = BeautifulSoup(
                        ipo.ipoGmpData["gmp_percent_calc"], "html.parser"
                    ).text.strip()
                else:
                    ipo.ipoGmpData = {}

            return response.success_response(
                status_code=200, data=jsonable_encoder(active_ipos)
            )


ipo_services = IPOService()
