
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from src.core.config import settings
from src.db.connection import get_session
from src.crud.user_crud import get_user
from src.models.user_model import User
from src.schemas.token_schema import TokenData
from src.api.controllers.user_controller import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(
    db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    if current_user.isDeleted: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User account is deleted")
    return current_user

def get_current_superuser(current_user: User = Depends(get_current_active_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    return current_user


def isAdmin(current_user: User = Depends(get_current_active_user)) -> bool:
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return True

def isLearner(current_user: User = Depends(get_current_active_user)) -> bool:
    if current_user.role.name != "learner":
        raise HTTPException(status_code=403, detail="Learner access required")
    return True


def isMentor(current_user: User = Depends(get_current_active_user)) -> bool:
    if current_user.role.name != "mentor":
        raise HTTPException(status_code=403, detail="Mentor access required")
    return True