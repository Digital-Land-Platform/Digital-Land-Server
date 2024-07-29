#!/usr/bin/env python3

"""
login.py

This module defines the authentication routes for the Digital Land
application using FastAPI. It provides an endpoint for user login 
that redirects to an external authentication service.

Routes:
    /login: Initiates the login process by redirecting users to 
            the authentication service.

Attributes:
    router (APIRouter): An instance of FastAPI's APIRouter to 
                        handle routing for authentication endpoints.
    client_id (str): The client ID for the authentication service.
    auth_domain (str): The domain of the authentication service.
    audience (str): The audience parameter for the authentication 
                    service.
    redirect_uri (str): The URI to redirect to after authentication.
"""

from fastapi import APIRouter
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()

client_id = os.getenv("CLIENT_ID", " ")
auth_domain = os.getenv("AUTH_DOMAIN", " ")
audience = os.getenv("AUDUENCE", " ")
rediredt_uri = os.getenv("REDIRECT_URI", " ")

@router.get("/login")
def login():
    """
    Initiates the login process by redirecting users to the 
    authentication service.

    Returns:
        RedirectResponse: A redirect response to the authentication 
                          service's authorization endpoint, 
                          including the necessary query parameters 
                          for authentication.
    """
    return RedirectResponse(
            f"https://{auth_domain}/authorize"
            "?response_type=code"
            f"&client_id={client_id}"
            f"&redirect_uri={rediredt_uri}"
            "&scope=offline_access openid profile email read:users"
            f"&audience={audience}"
        )