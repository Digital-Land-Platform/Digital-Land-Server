#!/usr/bin/env python3

from typing import Dict
from src.models.repository.userRepository import UserRepository
from src.models.User import User
from sqlalchemy.ext.asyncio import AsyncSession
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException, InternalServerErrorException, 
    NotFoundException
)

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def create_user(self, user: User) -> User:
        try:
            if not user:
                raise BadRequestException("Invalid user data.")
            return await self.user_repo.create_user(user)
        except Exception as e:
            raise InternalServerErrorException()
        
    async def update_user(self, user_id, user: Dict) -> User:
        try:
            if not user_id or not user:
                raise BadRequestException("Invalid user ID or data.")
            
            existing_user = await self.user_repo.get_user_by_id(user_id)
            if not existing_user:
                raise NotFoundException("User not found.")
            
            return await self.user_repo.update_user(user_id, user)
        except (NotFoundException, BadRequestException) as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
        
    async def delete_user(self, user_id: str) -> str:
        try:
            if not user_id:
                raise BadRequestException("Invalid user ID.")
            
            user = await self.user_repo.get_user_by_id(user_id)
            if not user:
                raise NotFoundException("User not found.")
            
            return await self.user_repo.delete_user(user_id)
        except (NotFoundException, BadRequestException) as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_user_by_id(self, user_id: int) -> User:
        try:
            return await self.user_repo.get_user_by_id(user_id)
        except Exception as e:
            raise InternalServerErrorException()
        
    async def get_user_by_email(self, email: str) -> User:
        try:
            return await self.user_repo.get_user_by_email(email)
        except Exception as e:
            raise InternalServerErrorException()

    async def get_all_users(self) -> list[User]:
        try:
            return await self.user_repo.get_all_users()
        except Exception as e:
            raise InternalServerErrorException()
