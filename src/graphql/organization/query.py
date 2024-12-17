import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
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
    @ExceptionHandler.handle_exceptions    
    async def get_organization(self, info, org_id: str) -> OrganizationType:
        organization = await organization_service.get_organization(org_id)
        return OrganizationType.from_orm(organization)

    @strawberry.field
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def get_organizations(self, info) -> list[OrganizationType]:
        organizations = await organization_service.get_all_organizations()
        return [OrganizationType.from_orm(organization) for organization in organizations]
