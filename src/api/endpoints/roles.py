
from fastapi import APIRouter, Depends, UploadFile, File
from sqlmodel import Session 
from typing import Annotated, Optional
from src.models.user_model import User 
from datetime import date 

from src.db.connection import get_session 
from src.schemas import user_schema
from src.api.controllers import user_controller
from src.api.endpoints.dependencies import get_current_active_user

router = APIRouter()

@router.get("/me", response_model=user_schema.UserProfile)
async def read_current_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)], 
    db: Session = Depends(get_session), 
    
):
    """
    Get current user's profile information.
    """
    return await user_controller.get_user_profile(db, current_user)


@router.patch("/me", response_model=user_schema.UserProfile)
async def update_current_user_profile(

    current_user: Annotated[User, Depends(get_current_active_user)], 
    db: Session = Depends(get_session), 
    
    user_update: user_schema.UserUpdate = Depends(), 
    profile_picture: Optional[UploadFile] = File(None),
):
    """
    Update current user's profile information.
    Supports partial updates.
    Profile picture can be uploaded or removed by passing an empty string for the field.
    """
    return await user_controller.update_user_profile(
        db, current_user, user_update, profile_picture
    )

@router.get("/me/role", response_model=user_schema.UserPublic)
async def read_current_user_role(
    current_user: Annotated[User, Depends(get_current_active_user)], 
    db: Session = Depends(get_session), 
    
    ):
    """
    Get current user's role information. (Replaces RoleController.get logic)
    """
    return await user_controller.get_user_role_info(current_user) 