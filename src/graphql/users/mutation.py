#!/usr/bin/env python

import strawberry
from .services import UserService
from .index import UserType
from models.User import User
from models.UserRole import UserRole
from config.database import db

@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def create_user(self, user_input: dict) -> UserType:
        try:
            user_service = UserService(db)
            user = User(**user_input)
            created_user = await user_service.create_user(user)
            return UserType.from_model(created_user)
        except Exception as e:
            raise Exception(f"Failed to create user: {e}")
    
    @strawberry.mutation
    async def update_user(self, user_input: dict) -> UserType:
        try:
            user_service = UserService(db)
            user = User(**user_input)
            updated_user = await user_service.update_user(user)
            return UserType.from_model(updated_user)
        except Exception as e:
            raise Exception(f"Failed to create user: {e}")
        
    @strawberry.mutation
    async def update_user_role(self, user_id: int, new_role: UserRole) -> UserType:
        try:
            user_service = UserService(db)
            updated_user = await user_service.update_user_role(user_id, new_role)
            return UserType.from_model(updated_user)
        except Exception as e:
            raise Exception(f"Failed to update user role: {e}")

    @strawberry.mutation
    async def delete_user(self, user_id: int) -> bool:
        try:
            user_service = UserService(db)
            return await user_service.delete_user(user_id)
        except Exception as e:
            raise Exception(f"Failed to delete user: {e}")
