#!/usr/bin/env python3
import strawberry
from typing import List
from .index import UserType
from .services import UserService
from config.database import db


user_service = UserService(db.SessionLocal())


@strawberry.type
class UserQuery:
    
    @strawberry.field
    async def get_users(self) -> List[UserType]:
        
        try:
            found_user = await user_service.get_all_users()
            return [UserType.from_model(user) for user in found_user]
        except Exception as e:
            raise Exception(f"Failed to get user: {e}")
    
    @strawberry.field
    async def get_user_email(self, email: str) -> UserType:
        try:
            found_user = await user_service.get_user_by_email(email)
            return UserType.from_model(found_user)
        except Exception as e:
            raise Exception(f"Failed to get user: {e}")

    @strawberry.field
    async def get_user_id(self, user_id: str) -> UserType:
        try:
            found_user = await user_service.get_user_by_id(user_id)
            return UserType.from_model(found_user)
        except Exception as e:
            raise Exception(f"Failed to get user: {e}")
        
    