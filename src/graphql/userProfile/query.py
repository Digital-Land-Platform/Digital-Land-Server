import strawberry
from strawberry.types import Info
from strawberry.directive import DirectiveValue
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from src.models.enums.UserRole import UserRole
from .types import UserProfileAuditLogType, UserProfileType, UserProfileInput
from src.models.UserProfile import UserProfile
from fastapi import HTTPException   
from .service import UserProfileService
from src.middleware.AuthManagment import AuthManagement
from config.database import db
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException
)


auth_management = AuthManagement()
user_profile_service = UserProfileService(db)

@strawberry.type
class UserProfile:

    @strawberry.field
    @ExceptionHandler.handle_exceptions
    async def get_user_profile(self, user_profile_id: DirectiveValue[str]) -> UserProfileType:
        user_profile = await user_profile_service.get_user_profile_by_id(user_profile_id)
        if not user_profile:
            raise BadRequestException(detail="User profile not found")
        return UserProfileType.from_model(user_profile)
    
    @strawberry.field
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def delete_user_profile(self, user_profile_id: DirectiveValue[str]) -> DirectiveValue[str]:
        deleted_profile = await user_profile_service.delete_user_profile(user_profile_id)
        return deleted_profile
    
    @strawberry.field
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def get_all_audit_logs(self, user_profile_id: DirectiveValue[str]) -> list[UserProfileAuditLogType]:
        audit_logs = await user_profile_service.get_all_audit_logs(user_profile_id)
        return [UserProfileAuditLogType.from_model(audit_log) for audit_log in audit_logs]
