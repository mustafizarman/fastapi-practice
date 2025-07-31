
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.crud import role_crud, user_crud
from src.schemas import role_schema
from src.models.role_model import Role

def get_all_roles(db: Session, skip: int = 0, limit: int = 100) -> list[Role]:
    return role_crud.get_roles(db, skip=skip, limit=limit)

def create_new_role(db: Session, role_create: role_schema.RoleCreate) -> Role:
    db_role = role_crud.get_role_by_name(db, name=role_create.name)
    if db_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role name already exists")
    return role_crud.create_role(db=db, role=role_create)

def update_existing_role(db: Session, role_id: int, role_update: role_schema.RoleUpdate) -> Role:
    db_role = role_crud.get_role(db, role_id=role_id)
    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    
    if role_update.name and role_update.name != db_role.name:
        if role_crud.get_role_by_name(db, name=role_update.name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New role name already exists")
            
    return role_crud.update_role(db=db, db_role=db_role, role_update=role_update)

def delete_role_by_id(db: Session, role_id: int) -> dict:
    db_role = role_crud.get_role(db, role_id=role_id)
    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    
    user_crud.set_default_role_for_users(db, deleted_role_id=role_id)
    
    role_crud.delete_role(db=db, db_role=db_role)
    return {"message": "Role deleted successfully and users re-assigned."}