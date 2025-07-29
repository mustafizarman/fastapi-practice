# app/crud/user_crud.py
from sqlmodel import Session, select
from src.models.user_model import User, UserBase
from src.schemas.user_schema import UserCreate, UserUpdate, UserCustomUpdate
from src.core.security import get_password_hash
from src.crud.role_crud import get_learner_role_id, get_role # Import get_role here
from src.core.logger import logger

def get_user(session: Session, user_id: int) -> User | None:
    return session.exec(select(User).where(User.id == user_id, User.isDeleted == False)).first()

def get_user_by_email(session: Session, email: str) -> User | None:
    user =  session.exec(select(User).where((User.email == email) & (User.isDeleted == False))).first()
    print("SQL user", user)
    return user

def get_user_by_username(session: Session, username: str) -> User | None:
    return session.exec(select(User).where(User.username == username, User.isDeleted == False)).first()

def get_users(session: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return session.exec(select(User).where(User.isDeleted == False).offset(skip).limit(limit)).all()

def get_users_by_role_id(session: Session, role_id: int) -> list[User]:
    return session.exec(select(User).where(User.role_id == role_id, User.isDeleted == False)).all()

def create_user(session: Session, user_create: UserCreate) -> User:
    hashed_password = get_password_hash(user_create.password)
    
    # Handle default role
    # role_id = user_create.role_id
    # if role_id is None:
    default_role_id = get_learner_role_id(session)
    if default_role_id is None:
        raise ValueError("Default 'learner' role not found. Please create it first.")
    role_id = default_role_id

    # Create User model instance
    db_user = User(
        email=user_create.email,
        username=user_create.email,
        hashed_password=hashed_password,
        # role_id=role_id,
        # profile_picture=user_create.profile_picture,
        # birthday=user_create.birthday,
        # designation=user_create.designation,
        # phone_number=user_create.phone_number,
        # is_active=user_create.is_active,
        # is_superuser=user_create.is_superuser
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def update_user(session: Session, db_user: User, user_update: UserCustomUpdate) -> User:
    logger.info(f"Original UserUpdate: {user_update}")
    update_data = user_update.model_dump(exclude_unset=True,  exclude_none=True)
    # update_data = {
    #     key: value
    #     for key, value in user_update.model_dump(exclude_unset=True).items()
    #     if value is not None
    # }

    logger.info(f"Filtered update_data: {update_data}")
    if update_data.get("password"):
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # Handle role_id update: ensure role exists if provided
    if "role_id" in update_data and update_data["role_id"] is not None:
        if not get_role(session, update_data["role_id"]):
            raise ValueError(f"Role with ID {update_data['role_id']} does not exist.")
    logger.info(f"Success Update")
    db_user.sqlmodel_update(update_data) # SQLModel's update method
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def delete_user(session: Session, db_user: User) -> User:
    db_user.isDeleted = True
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# Logic for on_delete=models.SET(get_default_role) when a Role is deleted
def set_default_role_for_users(session: Session, deleted_role_id: int):
    default_role_id = get_learner_role_id(session)
    if default_role_id:
        users_to_update = session.exec(select(User).where(User.role_id == deleted_role_id)).all()
        for user in users_to_update:
            user.role_id = default_role_id
            session.add(user)
        session.commit()
    else:
        print(f"Warning: Default 'learner' role not found. Users from deleted role {deleted_role_id} will have null role_id.")