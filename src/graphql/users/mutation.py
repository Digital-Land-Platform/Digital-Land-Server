#!/usr/bin/env python

from fastapi.exceptions import RequestValidationError
import strawberry
from .services import UserService
from .index import UserType, UserInput
from src.models.UserRole import UserRole
from src.models.User import User
from fastapi import HTTPException
from config.database import db

userService = UserService(db.SessionLocal())

@strawberry.type
class UserMutation:
        
    @strawberry.mutation
    async def register_user(self, user_input: UserInput) -> UserType:
        try:
            user_role = UserRole.ADMIN
            if user_input.user.user_role.value == UserRole.BUYER.value:
                user_role = UserRole.BUYER
            elif user_input.user.user_role.value == UserRole.LAND_OWNER.value:
                user_role = UserRole.LAND_OWNER
            elif user_input.user.user_role.value == UserRole.NOTARY.value:
                user_role = UserRole.NOTARY

            user_dict = {
                "name": user_input.user.name,
                "email": user_input.user.email,
                "password": user_input.user.password,
                "role": user_role
            }
            exist_user = await userService.get_user_by_email(user_dict["email"])
            if exist_user:
                raise HTTPException(status_code=400, detail="User email already exists")
            print("User dict: ", user_dict)
            new_user = User(**user_dict)
            user = await userService.create_user(new_user)
            if not user:
                raise HTTPException(status_code=400, detail="Failed to create user")
            return UserType.from_model(user)
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)
        except RequestValidationError as e:
            raise strawberry.exceptions.GraphQLError(str(e))

    @strawberry.mutation
    async def update_user(self, user_id: str, user_input: UserInput) -> UserType:
        try:
            user_role = UserRole.ADMIN
            if user_input.user.user_role.value == UserRole.BUYER.value:
                user_role = UserRole.BUYER
            elif user_input.user.user_role.value == UserRole.LAND_OWNER.value:
                user_role = UserRole.LAND_OWNER
            elif user_input.user.user_role.value == UserRole.NOTARY.value:
                user_role = UserRole.NOTARY
            
            user_dict = {
                "name": user_input.user.name,
                "email": user_input.user.email,
                "password": user_input.user.password,
                "role": user_role
            }
            print("User dict: ", user_dict)
            user = await userService.update_user(user_id, user_dict)
            if not user:
                raise HTTPException(status_code=400, detail="Failed to update user")
            return UserType.from_model(user)
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)
        except RequestValidationError as e:
            raise strawberry.exceptions.GraphQLError(str(e))

    @strawberry.mutation
    async def delete_user(self, user_id: str) -> str:
        try:
            result = await userService.delete_user(user_id)
            return result
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)
        except RequestValidationError as e:
            raise strawberry.exceptions.GraphQLError(str(e))