from sqlalchemy.orm import Session
from app.db.models.user import User
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

class UserCrud:
    def create_user(self, db: Session, name: str, username: str, email: str, password: str):
        db_user = User(name=name, username=username, email=email, password=password)
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered."
            )

    # Get all users
    def get_users(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(User).offset(skip).limit(limit).all()

    # Get a user by id
    def get_user_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    # Get a user by username
    def get_user_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    # Get a user by email
    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    # Update a user
    def update_user(self, db: Session, user_id: int, name: str = None, username: str = None, email: str = None, password: str = None):
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            if name:
                db_user.name = name
            if username:
                db_user.username = username
            if email:
                db_user.email = email
            if password:
                db_user.password = password
            db.commit()
            db.refresh(db_user)
            return db_user
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    # Delete a user
    def delete_user(self, db: Session, user_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return db_user
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

user_crud=UserCrud()