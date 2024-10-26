from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.UserProfileAuditLog import UserProfileAuditLog
from src.models.repository.UserProfileRepository import UserProfileRepository
from src.models.UserProfile import UserProfile
from src.models.repository.UserProfileAuditLogRepository import UserProfileAuditLogRepository


class UserProfileService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.u_p_repository = UserProfileRepository(self.db)
        self.u_p_a_l_repository = UserProfileAuditLogRepository(self.db)

    async def create_user_profile(self, userProfile: UserProfile) -> UserProfile:
        try:
            return await self.u_p_repository.create_user_profile(userProfile)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def update_user_profile(self, userProfileId: int, updatedUserProfile: dict) -> UserProfile:
        try:
            return await self.u_p_repository.update_user_profile(userProfileId, updatedUserProfile)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    async def get_user_profile_by_id(self, userProfileId: str) -> UserProfile:
        try:
            return await self.u_p_repository.get_user_profile_by_id(userProfileId)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def delete_user_profile(self, userProfileId: str) -> Optional[str]:
        try:
            return await self.u_p_repository.delete_user_profile(userProfileId)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    async def get_user_profile_by_user_id(self, userId: str) -> UserProfile:
        try:
            return await self.u_p_repository.get_user_profile_by_user_id(userId)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def check_phone_number(self, phone_number: str) -> UserProfile:
        try:
            return await self.u_p_repository.check_phone_number(phone_number)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def get_all_audit_logs(self, user_profile_id: str) -> list[UserProfileAuditLog]:
        try:
            return await self.u_p_a_l_repository.get_audit_logs(user_profile_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))