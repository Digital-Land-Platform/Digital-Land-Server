#!/usr/bin/python3

"""
token.py

This module defines the token route for the Digital Land application
using FastAPI. It provides an endpoint for exchanging an authorization
code for an access token.

Routes:
    /token: Exchanges an authorization code for an access token.

Attributes:
    router (APIRouter): An instance of FastAPI's APIRouter to handle 
                        routing for authentication token endpoints.
    client_id (str): The client ID for the authentication service.
    client_secret (str): The client secret for the authentication 
                         service.
    auth_domain (str): The domain of the authentication service.
    audience (str): The audience parameter for the authentication 
                    service.
    redirect_uri (str): The URI to redirect to after authentication.
"""

from fastapi import APIRouter, HTTPException
from src.models.User import User
from src.middleware.AuthManagment import AuthManagment
from src.graphql.users.services import UserService
from config.database import db
from src.models.UserRole import UserRole
import requests
import os

router = APIRouter()
auth_managment = AuthManagment()
userService = UserService(db.SessionLocal())

client_id = os.getenv("CLIENT_ID", " ")
client_secret = os.getenv("CLIENT_SECRET", " ")
auth_domain = os.getenv("AUTH_DOMAIN", " ")
rediredt_uri = os.getenv("REDIRECT_URI", " ")
audience = os.getenv("AUDUENCE", " ")

@router.get("/token")
async def get_access_token(code: str):
        """
        Exchanges an authorization code for an access token.

        Args:
            code (str): The authorization code received from the 
                        authentication service.

        Returns:
            str: The access token received from the authentication 
                service, or None if not found in the response.
        """
        payload = (
            "grant_type=authorization_code"
            f"&client_id={client_id}"
            f"&client_secret={client_secret}"
            f"&code={code}"
            f"&redirect_uri={rediredt_uri}"
            f"&audience={audience}"
        )
        headers = {"content-type": "application/x-www-form-urlencoded"}
        response = requests.post(f"https://{auth_domain}/oauth/token", payload, headers=headers)
        access_token = response.json().get("access_token")
        auth_managment.validate_token(access_token)
        user_info = auth_managment.get_user_info(access_token)
        if not user_info.get("email_verified"):
            raise HTTPException(status_code=400, detail="Failed to create user")
        exist_user = await userService.get_user_by_email(user_info.get("email"))
        if exist_user:
            return access_token
        else:
            user_data = {
                 "name": user_info.get("name"),
                "email": user_info.get("email"),
                "role": UserRole.BUYER
            }
            user = User(**user_data)
            await userService.create_user(user)
            return access_token