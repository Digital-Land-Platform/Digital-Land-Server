import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app, init_app
from src.startups.dbConn import startDBConnection


def test_home_route():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


def test_non_existent_route():
    client = TestClient(app)
    response = client.get("/non-existent-route")
    assert response.status_code == 404


def test_error_route():
    client = TestClient(app)
    response = client.get("/error")
    assert response.status_code == 400
