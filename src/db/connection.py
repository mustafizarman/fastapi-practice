# app/db/connection.py
from typing import List, Optional
from sqlmodel import SQLModel, Session, create_engine
from decouple import config as decouple_config # Using decouple for .env

DATABASE_URL = decouple_config("DATABASE_URL") # Decouple handles default "" itself

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env or environment variables.")

engine = create_engine(
    DATABASE_URL
    # ,
    # echo=True, # Set to False in production
    # connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

def init_db():
    print("creating db")
    # SQLModel.metadata.create_all(engine) # This is for initial table creation
    # For migrations, we'll use Alembic instead, so this call will usually be commented out
    # or used only for quick dev setup without Alembic.
    pass # We'll remove this from init_db() and rely on Alembic

def create_db_and_tables():
    """Utility to create tables for the first time or for testing."""
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session