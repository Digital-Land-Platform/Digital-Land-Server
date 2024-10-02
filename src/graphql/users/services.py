#!/usr/bin/env python3

from models.repository.userRepository import UserRepository
from models.User import User
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
    
    async def create_user(self, user: User) -> User:
        try:
            return await self.user_repo.create_user(user)
        except Exception as e:
            raise Exception(f"Failed to create user: {e}")
    
    async def update_user(self, user: User) -> User:
        try:
            return await self.user_repo.update_user(user)
        except Exception as e:
            raise Exception(f"Failed to update user: {e}")
    
    async def delete_user(self, user_id: int) -> bool:
        try:
            return await self.user_repo.delete_user(user_id)
        except Exception as e:
            raise Exception(f"Failed to delete user: {e}")

    async def get_all_users(self) -> list[User]:
        try:
            return await self.user_repo.get_all_users()
        except Exception as e:
            raise Exception(f"Failed to get all users: {e}")

    async def update_user_role(self, user_id: int, new_role: str) -> User:
        try:
            return await self.user_repo.update_user_role(user_id, new_role)
        except Exception as e:
            raise Exception(f"Failed to update user role: {e}")
