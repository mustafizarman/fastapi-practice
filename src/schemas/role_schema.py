# app/schemas/role_schema.py
from src.models.role_model import RoleBase, Role
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

# Input Schemas
class RoleCreate(RoleBase):
    pass

class RoleUpdate(SQLModel): # Use SQLModel for partial updates
    name: Optional[str] = None
    description: Optional[str] = None
    isDeleted: Optional[bool] = None

# Output Schemas (can be same as the model if no fields are hidden)
class RolePublic(RoleBase):
    id: int
    createdAt: datetime
    updatedAt: Optional[datetime]
    isDeleted: bool
    
    class Config:
        from_attributes = True # Or orm_mode = True in Pydantic v1.x