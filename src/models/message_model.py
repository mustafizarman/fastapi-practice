from sqlmodel import SQLModel, Field
from datetime import datetime

class Message(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    sender_id: int
    receiver_id: int
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
