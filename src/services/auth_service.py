# app/services/auth_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta

from src.crud.user_crud import get_user_by_email
from src.core.security import verify_password, create_access_token
from src.schemas.token_schema import Token
from src.models.user_model import User
from src.core.config import settings
from fastapi import Depends
from functools import partial

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_user_access_token(user: User) -> Token:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)

# This would replace Django's `update_last_login` signal
def update_last_login(db: Session, user: User):
    # SQLAlchemy models automatically update 'updatedAt' on modification
    # If you need a specific 'last_login' field, add it to your User model
    # and update it here. For simplicity, we're relying on 'updatedAt' for now.
    pass

