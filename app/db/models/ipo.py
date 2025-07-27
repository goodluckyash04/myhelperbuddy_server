from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base, engine
from app.utils.date_and_time import date


class IPO(Base):
    __tablename__ = "ipos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    gmp_id: Mapped[int] = mapped_column(Integer, nullable=True)
    company: Mapped[str] = mapped_column(String, nullable=False)
    company_url: Mapped[str] = mapped_column(String, nullable=True)
    logo_url: Mapped[str] = mapped_column(String, nullable=True)
    opening_date: Mapped[datetime] = mapped_column(nullable=True)
    closing_date: Mapped[datetime] = mapped_column(nullable=True)
    listing_date: Mapped[datetime] = mapped_column(nullable=True)
    listing_at: Mapped[str] = mapped_column(String, nullable=True)
    issue_price: Mapped[float] = mapped_column(nullable=True)
    total_issue_amount: Mapped[float] = mapped_column(nullable=True)
    lead_manager: Mapped[str] = mapped_column(String, nullable=True)
    lead_manager_url: Mapped[str] = mapped_column(String, nullable=True)
    url_folder_name: Mapped[str] = mapped_column(String, nullable=True)
    short_name: Mapped[str] = mapped_column(String, nullable=True)

    created_at = mapped_column(DateTime, default=date.get_today_date())
    updated_at = mapped_column(
        DateTime, default=date.get_today_date(), onupdate=date.get_today_date()
    )


Base.metadata.create_all(bind=engine)
