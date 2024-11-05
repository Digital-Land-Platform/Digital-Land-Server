import strawberry
from strawberry.types import Info
from strawberry.directive import DirectiveValue
from src.models.enums.UserRole import UserRole
from .types import UserProfileAuditLogType, UserProfileType, UserProfileInput
from src.models.UserProfile import UserProfile
from fastapi import HTTPException   
from .service import UserProfileService
from src.middleware.AuthManagment import AuthManagement
from config.database import db

auth_management = AuthManagement()
user_profile_service = UserProfileService(db)

@strawberry.type
class UserProfile:

    @strawberry.field
    async def get_user_profile(self, user_profile_id: DirectiveValue[str]) -> UserProfileType:
        try:
            user_profile = await user_profile_service.get_user_profile_by_id(user_profile_id)
            if not user_profile:
                raise HTTPException(status_code=400, detail="User profile not found")
            return UserProfileType.from_model(user_profile)
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)
    
    @strawberry.field
    @auth_management.role_required([UserRole.ADMIN])
    async def delete_user_profile(self, user_profile_id: DirectiveValue[str]) -> DirectiveValue[str]:
        try:
            deleted_profile = await user_profile_service.delete_user_profile(user_profile_id)
            if not deleted_profile:
                raise HTTPException(status_code=400, detail="Failed to delete user profile")
            return deleted_profile
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)
    
    @strawberry.field
    async def get_all_audit_logs(self, user_profile_id: DirectiveValue[str]) -> list[UserProfileAuditLogType]:
        try:
            audit_logs = await user_profile_service.get_all_audit_logs(user_profile_id)
            if not audit_logs:
                raise HTTPException(status_code=400, detail="No audit logs found")
            return [UserProfileAuditLogType.from_model(audit_log) for audit_log in audit_logs]
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)