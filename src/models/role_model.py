
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from src.models.user_model import User

class RoleBase(SQLModel):
    name: str = Field(unique=True, index=True, nullable=False)
    description: Optional[str] = Field(default=None)
    isDeleted: bool = Field(default=False)

class Role(RoleBase, table=True):
    __tablename__ = "roles" 

    id: Optional[int] = Field(default=None, primary_key=True)
    createdAt: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updatedAt: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    

    # Relationship to User (back_populates)
    users: List["User"] = Relationship(back_populates="role")

    def __repr__(self):
        return f"<Role(name='{self.name}')>"