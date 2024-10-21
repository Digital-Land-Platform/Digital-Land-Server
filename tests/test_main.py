import sys
import os
import pytest
from fastapi import FastAPI
from httpx import AsyncClient  # Async client for testing async routes

# Add the root directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import init_app

# Initialize the app
app = init_app()

@pytest.mark.asyncio
async def test_home_route():
    print("Running test_home_route")
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_non_existent_route():
    print("Running test_non_existent_route")
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/non-existent-route")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_error_route():
    print("Running test_error_route")
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/error")
    assert response.status_code == 400
    assert response.json() == {"detail": "This is a custom error message"}

if __name__ == "__main__":
    pytest.main()
