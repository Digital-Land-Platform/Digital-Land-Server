from typing import Optional
from sqlalchemy import select
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from src.models.UserProfile import UserProfile
from src.models.enums.AuditActions import AuditActions
from .UserProfileAuditLogRepository import UserProfileAuditLogRepository

class UserProfileRepository:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.u_p_a_l_repository = UserProfileAuditLogRepository(self.db)
    
    async def create_user_profile(self, userProfile: UserProfile) -> UserProfile:
        try:
            async with self.db:
                async with self.db.session as session:
                    session.add(userProfile)
                    await session.commit()
                    await session.refresh(userProfile)
                    await self.u_p_a_l_repository.create_audit_log({
                        "user_profile_id": userProfile.id,
                        "entity": self.__class__.__name__,
                        "new_value": userProfile.__dict__,
                        "action": AuditActions.CREATE
                    })
                    return userProfile
        except SQLAlchemyError as e:
            raise Exception(f"Failed to create user profile: {e}") 
    
    async def update_user_profile(self, userProfileId: int, updatedUserProfile: dict) -> UserProfile:
        try:
            async with self.db:
                async with self.db.session as session:
                    statement = select(UserProfile).where(UserProfile.id == userProfileId)
                    result = await session.execute(statement)
                    user_profile = result.scalar_one_or_none()
                    if not user_profile:
                        raise Exception("User profile not found")
                    old_value = user_profile.__dict__
                    for key, value in updatedUserProfile.items():
                        if value and hasattr(user_profile, key):
                            setattr(user_profile, key, value)
                    user_profile.updated_at = datetime.now(timezone.utc)
                    session.add(user_profile)
                    await session.commit()
                    await session.refresh(user_profile)
                    await self.u_p_a_l_repository.create_audit_log({
                        "user_profile_id": user_profile.id,
                        "entity": self.__class__.__name__,
                        "old_value": old_value,
                        "new_value": user_profile.__dict__,
                        "action": AuditActions.UPDATE
                    })
                    return user_profile
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Failed to update user profile: {e}")
    
    async def get_user_profile_by_id(self, user_profile_id: str) -> UserProfile:
        try:
            async with self.db:
                async with self.db.session as session:
                    statement = select(UserProfile).where(UserProfile.id == user_profile_id)
                    result = await session.execute(statement)
                    user_profile = result.scalar_one_or_none()
                    if not user_profile:
                        raise Exception("User profile not found")
                    return user_profile
        except SQLAlchemyError as e:
            raise Exception(f"Failed to fetch user profile by ID: {e}")
    
    async def delete_user_profile(self, user_profile_id: str) -> Optional[str]:
        try:
            async with self.db:
                async with self.db.session as session:
                    statement = select(UserProfile).where(UserProfile.id == user_profile_id)
                    result = await session.execute(statement)
                    user_profile = result.scalar_one_or_none()
                    if not user_profile:
                        raise Exception("User profile not found")
                    old_value = user_profile.__dict__
                    await session.delete(user_profile)
                    await session.commit()
                    await self.u_p_a_l_repository.create_audit_log({
                        "user_profile_id": user_profile_id,
                        "entity": self.__class__.__name__,
                        "old_value": old_value,
                        "action": AuditActions.DELETE
                    })
                    return f"User profile with ID: {user_profile_id} deleted successfully"
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Failed to delete user profile: {e}")
    
    async def get_user_profile_by_user_id(self, user_id: str) -> UserProfile:
        try:
            async with self.db:
                async with self.db.session as session:
                    statement = select(UserProfile).where(UserProfile.user_id == user_id)
                    result = await session.execute(statement)
                    user_profile = result.scalar_one_or_none()
                    return user_profile
        except SQLAlchemyError as e:
            raise Exception(f"Failed to fetch user profile by user ID: {e}")
    
    async def check_phone_number(self, phone_number: str) -> UserProfile:
        try:
            async with self.db:
                async with self.db.session as session:
                    statement = select(UserProfile).where(UserProfile.whatsapp_number == phone_number)
                    result = await session.execute(statement)
                    user_profile = result.scalar_one_or_none()
                    if user_profile:
                        raise Exception("Phone number already exists")
                    return user_profile
        except SQLAlchemyError as e:
            raise Exception(f"Failed to fetch user profile by phone number: {e}")
    
    async def check_identity_card_number(self, identity_card_number: str) -> UserProfile:
        try:
            async with self.db:
                async with self.db.session as session:
                    statement = select(UserProfile).where(UserProfile.identity_card_number == identity_card_number)
                    result = await session.execute(statement)
                    user_profile = result.scalar_one_or_none()
                    if user_profile:
                        raise Exception("Identity card number already exists")
                    return user_profile
        except SQLAlchemyError as e:
            raise Exception(f"Failed to fetch user profile by identity card number: {e}")