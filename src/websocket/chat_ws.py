from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict

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
async def chat_ws(websocket: WebSocket, sender_id: int, receiver_id: int):
    await manager.connect(sender_id, websocket)
    try:
        while True:
            message = await websocket.receive_text()

            # Optional: structure the message (you can include sender id, etc.)
            full_message = f"[User {sender_id}]: {message}"
            
            # Send to receiver
            await manager.send_private_message(full_message, receiver_id)

            # Optionally echo to sender as well
            await websocket.send_text(f"You: {message}")

    except WebSocketDisconnect:
        manager.disconnect(sender_id)
