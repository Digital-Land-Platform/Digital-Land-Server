import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .types import OrganizationStaffType, OrganizationStaffInput
from .services import OrganizationStaffService
from src.models.enums.OrganizationRole import OrganizationRole
from config.database import db
from src.middleware.AuthManagment import AuthManagement

auth_management = AuthManagement()
organization_staff_service = OrganizationStaffService(db)

@strawberry.type
class OrganizationStaffMutation:

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def create_organization_staff(self, organization_staff_data: OrganizationStaffInput) -> OrganizationStaffType:
        organization_staff_data = vars(organization_staff_data)
        organization_staff = await organization_staff_service.create_organization_staff(organization_staff_data)
        return await OrganizationStaffType.from_orm(db, organization_staff)

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def update_organization_staff(self, org_staff_id: str, org_staff_data: OrganizationStaffInput) -> OrganizationStaffType:
        org_staff_data = vars(org_staff_data)
        organization_staff = await organization_staff_service.update_organization_staff(org_staff_id, org_staff_data)
        return await OrganizationStaffType.from_orm(db, organization_staff)

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def delete_organization_staff(self, org_id: str) -> str:
        message = await organization_staff_service.delete_organization_staff(org_id)
        return message
