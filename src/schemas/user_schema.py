# app/schemas/user_schema.py
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel
from fastapi import Form, UploadFile

from src.schemas.role_schema import RolePublic
from src.models.user_model import UserBase # Import UserBase from your model

# Input Schemas
class UserCreate(UserBase):
    password: str # Password should be explicitly required for creation

class UserUpdate(SQLModel): # Use SQLModel for partial updates
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None # For password change
    profile_picture: Optional[str] = None
    birthday: Optional[date] = None
    designation: Optional[str] = None
    phone_number: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    isDeleted: Optional[bool] = None

class UserCustomUpdate(SQLModel):
    birthday: Optional[str] = Form(None)
    designation: Optional[str] = Form(None)
    phone_number: Optional[str] = Form(None)
    profile_picture: Optional[UploadFile] = None

# Output Schemas (User without hashed password, but with role details)
class UserPublic(UserBase):
    id: int
    createdAt: datetime
    updatedAt: Optional[datetime]
    # No hashed_password field in public schema
    role: Optional[RolePublic] = None # Embed role data

    class Config:
        from_attributes = True

# Specific for Profile (can be same as UserPublic or tailored)
class UserProfile(UserPublic):
    pass