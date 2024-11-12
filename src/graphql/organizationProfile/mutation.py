import strawberry
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
    @auth_management.role_required([UserRole.ADMIN, UserRole.BROKER, UserRole.NOTARY, UserRole.USER])
    async def create_organization_profile(self, info, organization_profile_input: OrganizationProfileInput) -> OrganizationProfileType:
        try:
            organization_profile_input = vars(organization_profile_input)
            organization_profile = await organization_profile_service.create_organization_profile(organization_profile_input)
            if not organization_profile:
                raise Exception("Failed to create Organization Profile")
            return OrganizationProfileType.from_orm(organization_profile)
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to create Organization Profile: {e}")

    @strawberry.mutation
    @auth_management.role_required([UserRole.ADMIN, UserRole.BROKER, UserRole.NOTARY, UserRole.USER])
    async def update_organization_profile(self, info, org_id: str, org_profile_data: OrganizationProfileInput) -> OrganizationProfileType:
        try:
            org_profile_data = vars(org_profile_data)
            organization_profile = await organization_profile_service.update_organization_profile(org_id, org_profile_data)
            if not organization_profile:
                raise Exception("Failed to update Organization Profile")
            return OrganizationProfileType.from_orm(organization_profile)
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to update Organization Profile: {e}")

    @strawberry.mutation
    @auth_management.role_required([UserRole.ADMIN, UserRole.BROKER, UserRole.NOTARY, UserRole.USER])
    async def delete_organization_profile(self, info, org_id: str) -> str:
        try:
            message = await organization_profile_service.delete_organization_profile(org_id)
            return message
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to delete Organization Profile: {e}")