# tests/conftest.py

import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from src.models.role_model import Role
from src.main import app
from src.db.connection import get_session  # Your real session dep

# ✅ Shared, persistent in-memory test DB
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # Critical for keeping schema between sessions
)

# ✅ Override FastAPI DB dependency
def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

# ✅ Create tables before each test function
@pytest.fixture(scope="function", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        learner_role = Role(name="learner")
        session.add(learner_role)
        session.commit()


    yield
    SQLModel.metadata.drop_all(engine)

# ✅ Test client
@pytest.fixture
def client():
    return TestClient(app)
