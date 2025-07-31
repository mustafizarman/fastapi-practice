from fastapi import APIRouter
from sqlmodel import select
from fastapi import APIRouter, Depends, UploadFile, File
from sqlmodel import Session 
from typing import Annotated, Optional
from src.models.message_model import Message 
from datetime import date 

from src.db.connection import get_session 
from src.crud.message_crud import get_messages
router = APIRouter()

@router.get("/history/{user1}/{user2}")
def get_chat_history(user1: int, user2: int, session: Session = Depends(get_session)):
    
    return get_messages(session, user1, user2)
