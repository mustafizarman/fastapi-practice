import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_hello(client):
    
    res = client.get("/hello")
    print("testing hello")
    assert res.status_code == 200
