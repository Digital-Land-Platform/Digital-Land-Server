from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.repository.userRepository import UserRepository
from src.models.UserProfileAuditLog import UserProfileAuditLog
from src.models.repository.UserProfileRepository import UserProfileRepository
from src.models.UserProfile import UserProfile
from src.models.repository.UserProfileAuditLogRepository import UserProfileAuditLogRepository
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException, InternalServerErrorException, 
    NotFoundException
)

class UserProfileService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.userProfileRepository = UserProfileRepository(self.db)
        self.userProfileAuditLogRepository = UserProfileAuditLogRepository(self.db)
        self.userRepository = UserRepository(db)

    async def create_user_profile(self, userProfile: UserProfile) -> UserProfile:
        try:
            if not userProfile:
                raise BadRequestException("Invalid user profile data.")
            
            return await self.userProfileRepository.create_user_profile(userProfile)
        except BadRequestException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def update_user_profile(self, userProfileId: int, updatedUserProfile: dict) -> UserProfile:
        try:
            if not updatedUserProfile:
                raise BadRequestException("Invalid user profile data.")
            
            existing_user_profile = await self.userProfileRepository.get_user_profile_by_id(userProfileId)
            if not existing_user_profile:
                raise NotFoundException("User profile not found.")
    
            return await self.userProfileRepository.update_user_profile(userProfileId, updatedUserProfile)
        except (NotFoundException, BadRequestException) as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
        
    async def get_user_profile_by_id(self, userProfileId: str) -> UserProfile:
        try:
            return await self.userProfileRepository.get_user_profile_by_id(userProfileId)
        except Exception as e:
            raise InternalServerErrorException()
    
    async def delete_user_profile(self, userProfileId: str) -> Optional[str]:
        try:
            if not userProfileId:
                raise BadRequestException("Invalid user profile ID.")
            
            existing_user_profile = await self.userProfileRepository.get_user_profile_by_id(userProfileId)
            if not existing_user_profile:
                raise NotFoundException("User profile not found.")
            
            return await self.userProfileRepository.delete_user_profile(userProfileId)
        except (NotFoundException, BadRequestException) as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
        
    async def get_user_profile_by_user_id(self, userId: str) -> UserProfile:
        try:
            if not userId:
                raise BadRequestException("Invalid user ID.")
            
            existing_user = await self.userRepository.get_user_by_id(userId)
            if not existing_user:
                raise NotFoundException("User not found.")
            
            return await self.userProfileRepository.get_user_profile_by_user_id(userId)
        except Exception as e:
            raise InternalServerErrorException()
    
    async def check_phone_number(self, phone_number: str) -> UserProfile:
        try:
            return await self.userProfileRepository.check_phone_number(phone_number)
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_all_audit_logs(self, user_profile_id: str) -> list[UserProfileAuditLog]:
        try:
            return await self.userProfileAuditLogRepository.get_audit_logs(user_profile_id)
        except Exception as e:
            raise InternalServerErrorException()
        