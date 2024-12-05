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

from datetime import datetime
from fastapi import APIRouter, HTTPException
from src.models.User import User
from src.middleware.AuthManagment import AuthManagement
from src.graphql.users.services import UserService
from config.database import db
from config.config import Config
from src.models.enums.UserRole import UserRole
from src.graphql.invitation.services import InvitationService
from src.models.enums.InvitationStatus import InvitationStatus
import requests
import os

router = APIRouter()
auth_managment = AuthManagement()
userService = UserService(db.SessionLocal())
invitation_service = InvitationService(db)

client_id = Config.get_env_variable("CLIENT_ID")
client_secret = Config.get_env_variable("CLIENT_SECRET")
auth_domain = Config.get_env_variable("AUTH_DOMAIN")
rediredt_uri = Config.get_env_variable("REDIRECT_URI2")
audience = Config.get_env_variable("AUDUENCE")

@router.get("/token")
async def get_access_token(code: str, state: str = None):
        """
        Exchanges an authorization code for an access token.

        Args:
            code (str): The authorization code received from the 
                        authentication service.

        Returns:
            str: The access token received from the authentication 
                service, or None if not found in the response.
        """
        try:
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
            print("access token", access_token)
            auth_managment.validate_token(access_token)
            user_info = auth_managment.get_user_info(access_token)
            if not user_info.get("email_verified"):
                raise HTTPException(status_code=400, detail="Failed to create user, Email is not verified")
            if state:
                invitation = await invitation_service.verify_invitation(state, user_info.get("email"))
                if not invitation:
                    raise HTTPException(status_code=400, detail="Failed to verify invitation")                    
            exist_user = await userService.get_user_by_email(user_info.get("email"))
            if exist_user:
                return access_token
            else:
                user_data = {
                "username": user_info.get("name"),
                "email": user_info.get("email"),
                "image": user_info.get("picture"),
                "role":  UserRole.USER,
                "verified": user_info.get("email_verified"),
                }
                user = User(**user_data)
                await userService.create_user(user)
                return access_token
        except Exception as e:
             print(e)