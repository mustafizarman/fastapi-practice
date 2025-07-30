from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt

from src.services import auth_service
from src.schemas import user_schema, token_schema
from src.models.user_model import User
from src.core.logger import logger
from src.core.config import settings  # Ensure you have a settings module for SECRET_KEY & ALGORITHM
from src.core.security import get_password_hash
from src.crud.user_crud import get_user_by_email, create_user 

def authenticate_and_create_token(db: Session, email: str, password: str) -> token_schema.Token:
    logger.info(f"Login attempt for: {email}")
    user = auth_service.authenticate_user(db, email, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f"Login User : {user.email}")
    auth_service.update_last_login(db, user)  # Optional: tracks login time
    logger.info(f"Login successful for: {user.email}")
    return auth_service.create_user_access_token(user)


def register_new_user(db: Session, user_create: user_schema.UserCreate) -> User:
     # Avoid circular import

    existing_user = get_user_by_email(db, user_create.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = create_user(session=db, user_create=user_create)
    return new_user


# def google_register_or_login(db: Session, email: str, first_name: str = "", last_name: str = "") -> User:
#     user = db.query(User).filter(User.email == email).first()

#     if not user:
#         user = User(
#             email=email,
#             username=email.split("@")[0],
#             first_name=first_name,
#             last_name=last_name,
#         )
#         db.add(user)
#         db.commit()
#         db.refresh(user)

#     return user


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=60)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def google_register_or_login(db: Session, email: str, first_name: str = "", last_name: str = "", picture="") -> User:
    print("email",email, picture)
    user = get_user_by_email(db, email)

    if not user:
        dummy_password = get_password_hash("google_oauth_user")
        local_pic_path = save_google_picture(picture)
        user = User(
            email=email,
            username=email.split("@")[0],
            first_name=first_name,
            last_name=last_name,
            hashed_password=dummy_password,
            auth_provider="google",
            profile_picture = local_pic_path
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    user = get_user_by_email(db, email)
    print("Full user",user)
    return user



PROFILE_PIC_DIR = "static/profile_pics"
import os
import requests
from uuid import uuid4
def save_google_picture(picture_url: str) -> str:
    """Download picture and save locally. Return relative path for DB."""
    if not picture_url:
        return ""

    try:
        os.makedirs(PROFILE_PIC_DIR, exist_ok=True)

        # Create a unique filename
        filename = f"{uuid4().hex}.jpg"
        filepath = os.path.join(PROFILE_PIC_DIR, filename)

        # Download and save image
        response = requests.get(picture_url)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)
            return filepath  # Or return relative like: f"{PROFILE_PIC_DIR}/{filename}"
        else:
            print("Failed to download profile picture.")
    except Exception as e:
        print("Error saving Google profile picture:", e)

    return ""