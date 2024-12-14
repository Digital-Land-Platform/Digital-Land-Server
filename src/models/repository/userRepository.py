#!/usr/bin/env python3
from datetime import datetime, timezone
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.models.User import User

class UserRepository(User):
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user: User) -> User:
        async with self.db as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
    
    async def update_user(self, user_id: str, updaed_user: Dict) -> User:
        async with self.db as session:
            statement = select(User).where(User.id == user_id)
            result = await session.execute(statement)
            user = result.scalar_one_or_none()
            if not user:
                raise None
            for key, value in updaed_user.items():
                if value and hasattr(user, key):
                    setattr(user, key, value)
            user.updated_at = datetime.now(timezone.utc)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def get_user_by_id(self, user_id: int) -> User:
        async with self.db as session:
            statement = select(User).where(User.id == user_id)
            result = await session.execute(statement)
            user = result.scalar_one_or_none()
            if not user:
                raise None
            return user

    async def get_all_users(self) -> list[User]:
        async with self.db as session:
            statement = select(User)
            result = await session.execute(statement)
            return result.scalars().all()

    async def get_user_by_email(self, email: str) -> User:
        async with self.db as session:
            statement = select(User).where(User.email == email)
            result = await session.execute(statement)
            return result.scalar_one_or_none()

    async def delete_user(self, user_id: str) -> str:
        async with self.db as session:
            statement = select(User).where(User.id == user_id)
            result = await session.execute(statement)
            user = result.scalar_one_or_none()
            if not user:
                raise False
            await session.delete(user)
            await session.commit()
            return True
        
    async def delete_all_users(self) -> bool:
        async with self.db as session:
            statement = select(User)
            result = await session.execute(statement)
            users = result.scalars().all()
            if not users or len(users) == 0:
                return False 
            for user in users:
                await session.delete(user)
            await session.commit()
            return True
