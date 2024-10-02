#!/usr/bin/env python3
import strawberry
from typing import List
from .index import UserType
from .services import UserService
from config.database import db

@strawberry.type
class UserQuery:
    @strawberry.field
    async def get_users(self) -> List[UserType]:
        try:
            user_service = UserService(db)
            users = await user_service.get_all_users()
            return [UserType.from_model(user) for user in users]
        except Exception as e:
            raise Exception(f"Failed to get users: {e}")

    @strawberry.field
    async def get_user(self, user_id: int) -> UserType:
        try:
            user_service = UserService(db)
            found_user = await user_service.get_user_by_id(user_id)
            return UserType.from_model(found_user)
        except Exception as e:
            raise Exception(f"Failed to get user: {e}")