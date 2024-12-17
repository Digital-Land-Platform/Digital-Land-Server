import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from src.graphql.organizationProfile.types import OrganizationProfileType
from src.graphql.organizationProfile.service import OrganizationProfileService
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole
from config.database import db
from src.middleware.ErrorHundlers.CustomErrorHandler import NotFoundException

auth_management = AuthManagement()
organization_profile_service = OrganizationProfileService(db)

@strawberry.type
class OrganizationProfileQuery:

    @strawberry.field
    @ExceptionHandler.handle_exceptions
    async def get_organization_profile(self, info, org_id: str) -> OrganizationProfileType:
        organization_profile = await organization_profile_service.get_organization_profile(org_id)
        if not organization_profile:
            raise NotFoundException("Organization Profile not found")
        return OrganizationProfileType.from_orm(organization_profile)

    @strawberry.field
    @auth_management.role_required([UserRole.ADMIN])
    async def get_organization_profiles(self, info) -> list[OrganizationProfileType]:
        organization_profiles = await organization_profile_service.get_all_organization_profiles()
        return [OrganizationProfileType.from_orm(organization_profile) for organization_profile in organization_profiles]
