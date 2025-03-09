from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import validates

from app.db.database import Base, engine
from app.utils.date_and_time import date


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    created_at = Column(DateTime, default=date.get_today_date())
    updated_at = Column(DateTime, default=date.get_today_date(), onupdate=date.get_today_date())

    def __repr__(self):
        return f"<User(name={self.name}, username={self.username})>"

    @validates('username')
    def validate_username(self, key, value):
        if not value:
            raise ValueError("Username is required")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not value:
            raise ValueError("Email is required")
        return value

Base.metadata.create_all(bind=engine)
