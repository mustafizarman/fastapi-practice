# app/models/user_model.py
from datetime import datetime, date
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    firstname:  Optional[str] = Field(default="", max_length=100)
    
    #lastname:  Optional[str] = Field(default="", max_length=100)
    
    
    profile_picture: Optional[str] = Field(default=None)
    birthday: Optional[date] = Field(default=None)
    designation: Optional[str] = Field(default=None, max_length=100)
    phone_number: Optional[str] = Field(default=None, max_length=20)
    
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    isDeleted: bool = Field(default=False, nullable=True)

    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")


class User(UserBase, table=True):
    __tablename__ = "users" # Explicitly define table name

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False) # Store hashed password
    auth_provider: str = Field(default="local", nullable=True)  # or "google"

    createdAt: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updatedAt: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Relationship to Role
    role: Optional["Role"] = Relationship(back_populates="users")

    def __repr__(self):
        return f"<User(email='{self.email}')>"

# Import Role at the end to avoid circular dependency for forward references
from src.models.role_model import Role