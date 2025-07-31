
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel
from fastapi import Form, UploadFile

from src.schemas.role_schema import RolePublic
from src.models.user_model import UserBase 

class UserCreate(UserBase):
    password: str 

class UserUpdate(SQLModel): 
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None 
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

class UserPublic(UserBase):
    id: int
    createdAt: datetime
    updatedAt: Optional[datetime]
    role: Optional[RolePublic] = None 

    class Config:
        from_attributes = True

class UserProfile(UserPublic):
    pass