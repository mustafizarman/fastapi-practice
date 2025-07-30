from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.message_model import Message
# app/crud/role_crud.py
from sqlmodel import Session, select
from sqlalchemy import or_, and_

def save_message_to_db(
    session: Session, sender_id: int, receiver_id: int, content: str
):
    message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    session.add(message)
    session.commit()
    session.refresh(message)

def get_messages(
    session: Session, user1_id: int, user2_id: int, limit: int = 100
):
    messages = (
        session.query(Message)
        .filter(
            or_(
                and_(Message.sender_id == user1_id, Message.receiver_id == user2_id),
                and_(Message.sender_id == user2_id, Message.receiver_id == user1_id)
            )
        )
        .order_by(Message.timestamp.asc())
        .limit(limit)
        .all()
    )
    return messages