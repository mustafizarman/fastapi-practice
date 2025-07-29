# app/api/controllers/user_controller.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile, File
from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field

from src.crud import user_crud, role_crud
from src.schemas import user_schema, role_schema
from src.models.user_model import User
from src.services import file_service
from src.core.security import get_password_hash

async def get_user_profile(db: Session, current_user: User) -> user_schema.UserProfile:
    # The user object is already loaded by the dependency, just return it
    return user_schema.UserProfile.model_validate(current_user)

async def update_user_profile(
    db: Session,
    current_user: User,
    user_update: user_schema.UserCustomUpdate,
    profile_picture_file: Optional[UploadFile] = File(None),
) -> user_schema.UserProfile:

    # Handle profile picture update
    if profile_picture_file:
        file_service.validate_image_extension(profile_picture_file.filename)
        # Delete old picture if it exists
        if current_user.profile_picture:
            file_service.delete_profile_picture(current_user.profile_picture)
        
        # Save new picture
        new_pic_path = await file_service.save_profile_picture(profile_picture_file, current_user.id)
        user_update.profile_picture = new_pic_path
    elif user_update.profile_picture is not None and user_update.profile_picture == "":
        # If client explicitly sends empty string, it means delete the picture
        if current_user.profile_picture:
            file_service.delete_profile_picture(current_user.profile_picture)
        user_update.profile_picture = None

    updated_user = user_crud.update_user(session=db, db_user=current_user, user_update=user_update)
    return user_schema.UserProfile.model_validate(updated_user)

async def get_user_role_info(current_user: User) -> role_schema.RolePublic:
    if not current_user.role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User has no assigned role.")
    return role_schema.RolePublic.model_validate(current_user.role)

def create_user(db: Session, user_in: user_schema.UserCreate) -> User:
    return user_crud.create_user(session=db, user=user_in)

def get_user_by_email(db: Session, email: str) -> User | None:
    return user_crud.get_user_by_email(session=db, email=email)

# No direct "NavController" equivalent, data can be fetched from UserProfile directly
# or by combining relevant user/role data in a new schema if needed for frontend nav.


def get_all_user_profile(db: Session) -> list[User] | None:
    return user_crud.get_users(session=db)