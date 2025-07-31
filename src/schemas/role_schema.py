
from src.models.role_model import RoleBase, Role
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

class RoleCreate(RoleBase):
    pass

class RoleUpdate(SQLModel): 
    name: Optional[str] = None
    description: Optional[str] = None
    isDeleted: Optional[bool] = None

class RolePublic(RoleBase):
    id: int
    createdAt: datetime
    updatedAt: Optional[datetime]
    isDeleted: bool
    
    class Config:
        from_attributes = True 