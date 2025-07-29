# app/api/routers.py
from fastapi import APIRouter
from src.core.config import settings
from src.api.endpoints import auth, users, roles
from src.websocket import chat_ws 
api_router = APIRouter()

api_router.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
api_router.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
api_router.include_router(roles.router, prefix=f"{settings.API_V1_STR}/roles", tags=["Roles"])
api_router.include_router(chat_ws.router, prefix=f"{settings.API_V1_STR}/chats", tags=["chats"])