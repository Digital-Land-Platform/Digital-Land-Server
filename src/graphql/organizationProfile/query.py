import strawberry
from src.graphql.organizationProfile.types import OrganizationProfileType
from src.graphql.organizationProfile.service import OrganizationProfileService
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole
from config.database import db

auth_management = AuthManagement()
organization_profile_service = OrganizationProfileService(db)

@strawberry.type
class OrganizationProfileQuery:

    @strawberry.field
    @auth_management.role_required([UserRole.ADMIN, UserRole.BROKER, UserRole.NOTARY, UserRole.USER])
    async def get_organization_profile(self, info, org_id: str) -> OrganizationProfileType:
        try:
            organization_profile = await organization_profile_service.get_organization_profile(org_id)
            if not organization_profile:
                raise Exception("Organization Profile not found")
            return OrganizationProfileType.from_orm(organization_profile)
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to get Organization Profile: {e}")

    @strawberry.field
    @auth_management.role_required([UserRole.ADMIN])
    async def get_organization_profiles(self, info) -> list[OrganizationProfileType]:
        try:
            organization_profiles = await organization_profile_service.get_all_organization_profiles()
            return [OrganizationProfileType.from_orm(organization_profile) for organization_profile in organization_profiles]
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to get Organization Profiles: {e}")
