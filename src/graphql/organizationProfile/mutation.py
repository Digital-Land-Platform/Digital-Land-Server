import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .types import OrganizationProfileType, OrganizationProfileInput
from .service import OrganizationProfileService
from config.database import db
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole

auth_management = AuthManagement()
organization_profile_service = OrganizationProfileService(db)

@strawberry.type
class OrganizationProfileMutation:

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def create_organization_profile(self, info, organization_profile_input: OrganizationProfileInput) -> OrganizationProfileType:
        organization_profile_input = vars(organization_profile_input)
        organization_profile = await organization_profile_service.create_organization_profile(organization_profile_input)
        return OrganizationProfileType.from_orm(organization_profile)

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def update_organization_profile(self, info, org_id: str, org_profile_data: OrganizationProfileInput) -> OrganizationProfileType:
        org_profile_data = vars(org_profile_data)
        organization_profile = await organization_profile_service.update_organization_profile(org_id, org_profile_data)
        return OrganizationProfileType.from_orm(organization_profile)

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def delete_organization_profile(self, info, org_id: str) -> str:
        message = await organization_profile_service.delete_organization_profile(org_id)
        return message
