#!/usr/bin/env python3
from datetime import datetime, timezone
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from src.models.User import User


class UserRepository(User):
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user: User) -> User:
        try:
            async with self.db as session:
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
        except SQLAlchemyError as e:
            raise Exception(f"Failed to create user: {e}")
    
    async def update_user(self, user_id: str, updaed_user: Dict) -> User:
        try:
            async with self.db as session:
                statement = select(User).where(User.id == user_id)
                result = await session.execute(statement)
                user = result.scalar_one_or_none()
                if not user:
                     raise Exception("User not found")
                for key, value in updaed_user.items():
                     if value and hasattr(user, key):
                        setattr(user, key, value)
                user.updated_at = datetime.now(timezone.utc)
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Failed to update user: {e}")

    async def get_user_by_id(self, user_id: int) -> User:
        try:
            async with self.db as session:
                statement = select(User).where(User.id == user_id)
                result = await session.execute(statement)
                user = result.scalar_one_or_none()
                if not user:
                    raise Exception("User not found")
                return user
        except SQLAlchemyError as e:
            raise Exception(f"Failed to fetch user by ID: {e}")

    async def get_all_users(self) -> list[User]:
        try:
            async with self.db as session:
                statement = select(User)
                result = await session.execute(statement)
                return result.scalars().all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to fetch all users: {e}")

    async def get_user_by_email(self, email: str) -> User:
        try:
            async with self.db as session:
                statement = select(User).where(User.email == email)
                result = await session.execute(statement)
                return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to fetch user by username from repository: {e}")

    async def delete_user(self, user_id: str) -> str:
        try:
            async with self.db as session:
                statement = select(User).where(User.id == user_id)
                result = await session.execute(statement)
                user = result.scalar_one_or_none()
                if not user:
                     raise Exception("User not found")
                await session.delete(user)
                await session.commit()
                return f"User with ID: {user_id} deleted successfully"
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Failed to delete user: {e}")
