#!/usr/bin/python3

"""
AuthManagment.py

This module defines the AuthManagement class for handling JWT
authentication and user information retrieval in the Digital
Land App. It provides methods to validate JWT tokens and fetch
user information from the authentication service.

Classes:
    AuthManagement: Handles JWT token validation and user information
                    retrieval.

Attributes:
    auth_domain (str): The domain of the authentication service.
    audience (str): The audience parameter for the authentication 
                    service.
"""

from functools import wraps
from fastapi import HTTPException
import requests
import os
from jose import jws, jwt, ExpiredSignatureError, JWTError, JWSError
from jose.exceptions import JWTClaimsError
from src.graphql.users.services import UserService
from src.models.UserRole import UserRole
from config.database import db

auth_domain = os.getenv("AUTH_DOMAIN", " ")
audience = os.getenv("AUDUENCE", " ")
userService = UserService(db.SessionLocal())

class AuthManagment():
    """
    AuthManagement Class

    This class provides methods for managing JWT authentication,
    including validation of tokens and retrieval of user information.

    Attributes:
        jwks_endpoint (str): The endpoint for retrieving JSON Web Key
                             Sets (JWKS) for public key validation.
        jwks (list): A list of public keys retrieved from the JWKS 
                     endpoint.
    """

    def __init__(self):
        """
        Initializes the AuthManagement instance by retrieving the 
        JWKS from the authentication service.
        """
        try:
            self.jwks_endpoint = f"https://{auth_domain}/.well-known/jwks.json"
            self.jwks = requests.get(self.jwks_endpoint).json()["keys"]
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve JWKS: {str(e)}")
        except KeyError:
            raise HTTPException(status_code=500, detail="JWKS response did not contain expected keys.")


    def find_public_key(self, kid):
        """
        Finds the public key corresponding to the given key ID (kid).

        Args:
            kid (str): The key ID to look for in the JWKS.

        Returns:
            dict: The public key dictionary corresponding to the kid,
                  or None if not found.
        """
        for key in self.jwks:
            if key["kid"] == kid:
                return key


    def validate_token(self, get_token: str):
            """
            Validates the given JWT token and decodes its payload.

            Args:
                get_token (str): The JWT token to validate.

            Returns:
                dict: The decoded token payload if validation succeeds.

            Raises:
                HTTPException: If token validation fails with a 401 status code.
            """
            try:
                unverified_headers = jws.get_unverified_header(get_token)
                token_payload = jwt.decode(
                    token=get_token,
                    key=self.find_public_key(unverified_headers["kid"]),
                    audience=f"{audience}",
                    algorithms="RS256",
                )
                return token_payload
            except (
                ExpiredSignatureError,
                JWTError,
                JWTClaimsError,
                JWSError,
            ) as error:
                raise HTTPException(status_code=401, detail=str(error))

    def get_user_info(self, token):
        """
        Retrieves user information from the authentication service using
        the provided token.

        Args:
            token (str): The JWT token to use for authorization.

        Returns:
            dict: The user information retrieved from the service.

        Raises:
            HTTPException: If the request to the /userinfo endpoint fails or
                        if the response cannot be parsed as JSON.
        """
        url = f"https://{auth_domain}/userinfo"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        # Check if the response status code is not 200 (OK)
        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid or expired token")
        elif response.status_code == 403:
            raise HTTPException(status_code=403, detail="Forbidden: You do not have access to this resource")
        elif response.status_code != 200:
            # Catch all other non-success status codes
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error fetching user info: {response.text}"
            )

        # Try to parse the response as JSON
        try:
            return response.json()
        except ValueError:
            raise HTTPException(status_code=500, detail="Failed to parse user info response")

    def role_required(self, required_roles):
        """
        Decorator to enforce role-based access control (RBAC) on protected
        endpoints. Checks if the authenticated user has one of the required
        roles.

        Args:
            required_roles (list): A list of roles authorized to access the
                                   endpoint.

        Returns:
            func: The decorated function, allowing access only if the user
                  has the required role.

        Raises:
            HTTPException: If the authorization header is missing, or if the
                           user's role is not one of the required roles, with
                           a 403 status code.
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                info = kwargs.get('info')  # For GraphQL, you'll get `info` from the arguments
                authorization_header = info.context["request"].headers.get("authorization")
                if not authorization_header:
                    raise HTTPException(status_code=403, detail="Authorization header missing")
                
                # Assuming `auth_management.get_user_info` returns user role info
                token = authorization_header.split("Bearer ")[1]
                user_info = self.get_user_info(token)
                user = await userService.get_user_by_email(user_info.get("email"))  # Or however roles are stored
                
                role = user.role
                if role not in required_roles:
                    raise HTTPException(status_code=403, detail="Access forbidden: UnAuthorized role")
                
                return await func(*args, **kwargs)
            return wrapper
        return decorator
