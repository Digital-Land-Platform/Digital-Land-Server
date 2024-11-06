import strawberry
from .types import OrganizationType, OrganizationInput
from .service import OrganizationService
from src.models.enums.UserRole import UserRole
from src.middleware.AuthManagment import AuthManagement
from config.database import db

organization_service = OrganizationService(db)
auth_management = AuthManagement()

@strawberry.type
class OrganizationQuery:

    @strawberry.field
    @auth_management.role_required([UserRole.ADMIN, UserRole.BROKER, UserRole.NOTARY, UserRole.USER])
    async def get_organization(self, org_id: str) -> OrganizationType:
        try:
            organization = await organization_service.get_organization(org_id)
            if not organization:
                raise Exception("Organization not found")
            return OrganizationType.from_orm(organization)
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to get Organization: {e}")

    @strawberry.field
    @auth_management.role_required([UserRole.ADMIN, UserRole.BROKER, UserRole.NOTARY, UserRole.USER])
    async def get_organizations(self) -> list[OrganizationType]:
        try:
            organizations = await organization_service.get_all_organizations()
            return [OrganizationType.from_orm(organization) for organization in organizations]
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to get Organizations: {e}")