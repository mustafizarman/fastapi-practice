# app/crud/role_crud.py
from sqlmodel import Session, select
from src.models.role_model import Role, RoleBase
from src.schemas.role_schema import RoleCreate, RoleUpdate

def get_role(session: Session, role_id: int) -> Role | None:
    return session.exec(select(Role).where(Role.id == role_id, Role.isDeleted == False)).first()

def get_role_by_name(session: Session, name: str) -> Role | None:
    return session.exec(select(Role).where(Role.name == name, Role.isDeleted == False)).first()

def get_roles(session: Session, skip: int = 0, limit: int = 100) -> list[Role]:
    return session.exec(select(Role).where(Role.isDeleted == False).offset(skip).limit(limit)).all()

def create_role(session: Session, role_create: RoleCreate) -> Role:
    db_role = Role.model_validate(role_create) # SQLModel's way to create from Pydantic
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role

def update_role(session: Session, db_role: Role, role_update: RoleUpdate) -> Role:
    # Apply updates from schema to model
    role_data = role_update.model_dump(exclude_unset=True)
    db_role.sqlmodel_update(role_data) # SQLModel's update method

    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role

def delete_role(session: Session, db_role: Role) -> Role:
    db_role.isDeleted = True
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role

# Helper to get the ID of the 'learner' role
def get_learner_role_id(session: Session) -> int | None:
    learner_role = get_role_by_name(session, name="learner")
    return learner_role.id if learner_role else None

# Helper to get the 'superadmin' user's ID
def get_superadmin_user_id(session: Session) -> int | None:
    superadmin_role = get_role_by_name(session, name='superadmin')
    if superadmin_role:
        from src.crud.user_crud import get_users_by_role_id # Avoid circular import at top
        superadmin_users = get_users_by_role_id(session, role_id=superadmin_role.id)
        if superadmin_users:
            return superadmin_users[0].id
    return None