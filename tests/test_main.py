import sys
import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Add the root directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Initialize the app
app = app

def test_home_route():
    print("Running test_home_route")
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200

def test_non_existent_route():
    print("Running test_non_existent_route")
    client = TestClient(app)
    response = client.get("/non-existent-route")
    assert response.status_code == 404

def test_error_route():
    print("Running test_error_route")
    client = TestClient(app)
    response = client.get("/error")
    assert response.status_code == 400
    assert response.json() == {"detail": "This is a custom error message"}

if __name__ == "__main__":
    pytest.main()