from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
from src.crud.message_crud import *
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import Annotated, Optional

from src.db.connection import get_session

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)

    async def send_private_message(self, message: str, receiver_id: int):
        receiver_ws = self.active_connections.get(receiver_id)
        if receiver_ws:
            await receiver_ws.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/chat/{sender_id}/{receiver_id}")
async def chat_ws(websocket: WebSocket, sender_id: int, receiver_id: int, session: Session = Depends(get_session)):
    await manager.connect(sender_id, websocket)
    try:
        while True:
            message = await websocket.receive_text()

            full_message = f"[User {sender_id}]: {message}"
            
            save_message_to_db(session=session, sender_id=sender_id, receiver_id=receiver_id, content=message)

            await manager.send_private_message(full_message, receiver_id)
            await websocket.send_text(f"You: {message}")

    except WebSocketDisconnect:
        manager.disconnect(sender_id)
