from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import Annotated, Optional

from src.db.connection import get_session
from src.schemas import user_schema
from src.models.user_model import User
from src.api.controllers import user_controller
from src.api.endpoints.dependencies import get_current_active_user, isLearner, isAdmin, isMentor
from src.core.logger import logger
from typing import List
router = APIRouter()

@router.get("/me", response_model=user_schema.UserProfile)
async def read_current_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_session)
    ):
    """
    Get current user's profile information.
    """
    return await user_controller.get_user_profile(db, current_user)


@router.patch("/me", response_model=user_schema.UserProfile)
async def update_current_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_update: Annotated[user_schema.UserCustomUpdate, Depends()],
    profile_picture: Optional[UploadFile] = File(None),
    db: Session = Depends(get_session),
):
    logger.info(f"user_update: {user_update}")
    return await user_controller.update_user_profile(
        db, current_user, user_update, profile_picture_file=profile_picture
    )


@router.get("/me/role", response_model=user_schema.RolePublic)
async def read_current_user_role(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Get current user's role information. (Replaces RoleController.get logic)
    """
    return await user_controller.get_user_role_info(current_user)


@router.get("/me/authcheck")
def getAuthCheck(
    current_user: Annotated[User, Depends(get_current_active_user)],
    is_mentor: bool = Depends(isMentor),
):
    """
    Get current user's role information. (Replaces RoleController.get logic)
    """
    
    return {
        "status": "Access granted",
        "user": current_user.username,
        "role": current_user.role.name,
        "isMentor": is_mentor,
    }


@router.get("/allusers", response_model=List[user_schema.UserProfile])
async def read_current_user_profile(
    db: Session = Depends(get_session)
    ):
    """
    Get current user's profile information.
    """
    return  user_controller.get_all_user_profile(db)