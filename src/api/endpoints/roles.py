# app/api/endpoints/users.py
from fastapi import APIRouter, Depends, UploadFile, File
from sqlmodel import Session # <-- Import Session from sqlmodel
from typing import Annotated, Optional
from src.models.user_model import User # <-- Import User model for type hint
from datetime import date # Add this import if birthday field is used in schema directly

from src.db.connection import get_session # <-- Corrected import
from src.schemas import user_schema
from src.api.controllers import user_controller
from src.api.endpoints.dependencies import get_current_active_user

router = APIRouter()

@router.get("/me", response_model=user_schema.UserProfile)
async def read_current_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)], # <-- Changed 'any' to 'User'
    db: Session = Depends(get_session), # <-- Changed to get_session
    
):
    """
    Get current user's profile information.
    """
    return await user_controller.get_user_profile(db, current_user)


@router.patch("/me", response_model=user_schema.UserProfile)
async def update_current_user_profile(
    # Required dependencies first
    current_user: Annotated[User, Depends(get_current_active_user)], # <-- Changed 'any' to 'User'
    db: Session = Depends(get_session), # <-- Changed to get_session
    
    # Then the other parameters
    user_update: user_schema.UserUpdate = Depends(), # If this is a form/query param, it's fine here
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
    current_user: Annotated[User, Depends(get_current_active_user)], # <-- Changed 'any' to 'User'
    db: Session = Depends(get_session), # Add db dependency (optional, but good practice if controller uses it)
    
    ):
    """
    Get current user's role information. (Replaces RoleController.get logic)
    """
    # If the controller doesn't need db, you can remove db from this endpoint's signature
    return await user_controller.get_user_role_info(current_user) # Removed db if not needed in controller