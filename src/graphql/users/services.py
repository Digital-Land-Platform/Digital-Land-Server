#!/usr/bin/env python3

from fastapi import HTTPException
from typing import Dict
from src.models.repository.userRepository import UserRepository
from src.models.User import User
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def create_user(self, user: User) -> User:
        try:
            return await self.user_repo.create_user(user)
        except Exception as e:
            raise Exception(f"Failed to create user: {e}")
        
    async def update_user(self, user_id, user: Dict) -> User:
        try:
            return await self.user_repo.update_user(user_id, user)
        except Exception as e:
            raise Exception(f"Failed to update user: {e}")
        
    async def delete_user(self, user_id: str) -> str:
        try:
            return await self.user_repo.delete_user(user_id)
        except Exception as e:
            raise Exception(f"Failed to delete user: {e}")
    
    async def get_user_by_id(self, user_id: int) -> User:
        try:
            return await self.user_repo.get_user_by_id(user_id)
        except Exception as e:
            raise Exception(f"Failed to get user by ID: {e}")
        
    async def get_user_by_email(self, email: str) -> User:
        try:
            return await self.user_repo.get_user_by_email(email)
        except Exception as e:
            raise Exception(f"Failed to get user by username: {e}")

    async def get_all_users(self) -> list[User]:
        try:
            return await self.user_repo.get_all_users()
        except Exception as e:
            raise Exception(f"Failed to get all users: {e}")
