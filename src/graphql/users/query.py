#!/usr/bin/python3

"""
query.py

This module defines the UserQuery class for handling GraphQL queries
related to user data in the Digital Land application. It provides
methods to access protected data, ensuring that the user is
authenticated and authorized.

Classes:
    UserQuery: Contains methods for querying user-related data.

Attributes:
    auth_management (AuthManagment): Instance of AuthManagment for
                                     handling authentication and authorization.
    user_service (UserService): Instance of UserService for interacting with
                                the user repository.
"""

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
import strawberry
from strawberry.types import Info
from strawberry.directive import DirectiveValue
from typing import List
from src.models.enums.UserRole import UserRole
from src.middleware.AuthManagment import AuthManagement
from .types import UserType
from .services import UserService
from config.database import db

auth_managment = AuthManagement()
user_service = UserService(db.SessionLocal())


@strawberry.type
class UserQuery:
    """
    UserQuery Class

    This class contains methods to handle GraphQL queries related to
    user data, including both protected and general user data.
    The methods ensure that only authenticated and authorized users
    can access the protected data.

    Methods:
        protected_data(info): Retrieves protected user data if the user
                              is authenticated.
        get_users(info): Retrieves a list of all users for users with
                         the "ADMIN" role.
        get_user_email(email): Retrieves user data by email.
        get_user_id(user_id): Retrieves user data by user ID.
    """

    @strawberry.field
    def protected_data(self, info: Info) -> DirectiveValue[str]:
        """
        Retrieves protected data for the authenticated user.

        Args:
            info (str): The GraphQL info object, which contains context
                         for the request.

        Returns:
            Optional[str]: A message indicating access to protected data,
                            including the user's name and email.

        Raises:
            HTTPException: If token validation fails or if the user
                            email is not verified, a 400 status code
                            is returned.
        """
        try:
            authorization_header = info.context["request"].headers.get("authorization")
            if authorization_header and authorization_header.startswith("Bearer "):
                token = authorization_header.split("Bearer ")[1]
            else:
                raise HTTPException(status_code=400, detail="Failed to create user")
            auth_managment.validate_token(token)
            user_info = auth_managment.get_user_info(token)
            if not user_info.get("email_verified"):
                raise HTTPException(status_code=400, detail="Failed to create user")
            
            return f"Endpoint is protected, can accessed by {user_info.get('given_name')} {user_info.get('email')}"
            
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)
        except RequestValidationError as e:
            raise strawberry.exceptions.GraphQLError(str(e))

    @strawberry.field
    @auth_managment.role_required([UserRole.ADMIN])
    async def get_users(self, info: Info) -> List[UserType]:
        """
        Retrieves a list of all users in the system.

        Args:
            info (Info): The GraphQL info object containing context for the request.

        Returns:
            List[UserType]: A list of users retrieved from the database.

        Raises:
            Exception: If there is a failure in retrieving user data from the database.
        """
        try:
            found_user = await user_service.get_all_users()
            return [UserType.from_model(user) for user in found_user]
        except Exception as e:
            raise Exception(f"Failed to get user: {e}")
    
    @strawberry.field
    @auth_managment.role_required([UserRole.ADMIN, UserRole.USER, UserRole.NOTARY])
    async def get_user_email(self, info:Info, email: DirectiveValue[str]) -> UserType:
        """
        Retrieves a user by their email.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            UserType: The user data corresponding to the given email.

        Raises:
            Exception: If there is a failure in retrieving user data from the database.
        """

        try:
            found_user = await user_service.get_user_by_email(email)
            return UserType.from_model(found_user)
        except Exception as e:
            raise Exception(f"Failed to get user: {e}")

    @strawberry.field
    async def get_user_id(self, user_id: DirectiveValue[str]) -> UserType:
        """
        Retrieves a user by their ID.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            UserType: The user data corresponding to the given ID.

        Raises:
            Exception: If there is a failure in retrieving user data from the database.
        """
        try:
            found_user = await user_service.get_user_by_id(user_id)
            return UserType.from_model(found_user)
        except Exception as e:
            raise Exception(f"Failed to get user: {e}")

