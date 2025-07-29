import sqlmodel 
from sqlmodel import SQLModel, Session
from .connection import DATABASE_URL

# if DATABASE_URL == "":
#     raise NotImplementedError("DATABASE_URL not set")


# engine = sqlmodel.create_engine(DATABASE_URL)


# def init_db():
#     print("creating db")
#     SQLModel.metadata.create_all(engine)

# def get_session():
#     with Session(engine) as session:
#         yield session 