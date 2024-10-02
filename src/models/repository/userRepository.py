#!/usr/bin/env python3

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from models.User import User


class UserRepository(User):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: User) -> User:
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Failed to create user: {e}")
    
    async def update_user(self, user_id: int, **kwargs) -> User:
        try:
            statement = select(User).where(User.id == user_id)
            result = await self.db.execute(statement)
            user = result.scalar_one_or_none()
            if not user:
                raise Exception("User not found")

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Failed to update user: {e}")

    async def get_user_by_id(self, user_id: int) -> User:
        try:
            statement = select(User).where(User.id == user_id)
            result = await self.db.execute(statement)
            user = result.scalar_one_or_none()
            if not user:
                raise Exception("User not found")
            return user
        except SQLAlchemyError as e:
            raise Exception(f"Failed to fetch user by ID: {e}")

    async def get_user_by_username(self, username: str) -> User:
        try:
            statement = select(User).where(User.username == username)
            result = await self.db.execute(statement)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to fetch user by username: {e}")

    async def get_all_users(self) -> list[User]:
        try:
            statement = select(User)
            result = await self.db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to fetch all users: {e}")

    async def delete_user(self, user_id: int) -> bool:
        try:
            statement = select(User).where(User.id == user_id)
            result = await self.db.execute(statement)
            user = result.scalar_one_or_none()
            if not user:
                raise Exception("User not found")

            await self.db.delete(user)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Failed to delete user: {e}")

    async def update_user_role(self, user_id: int, new_role: str) -> User:
        try:
            return await self.update_user(user_id, role=new_role)
        except Exception as e:
            raise Exception(f"Failed to update user role: {e}")