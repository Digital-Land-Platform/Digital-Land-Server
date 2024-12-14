import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from src.middleware.ErrorHundlers.CustomErrorHandler import NotFoundException
from src.middleware.AuthManagment import AuthManagement

from config.database import db
from .types import OrganizationStaffType, OrganizationStaffInput
from .services import OrganizationStaffService

auth_management = AuthManagement()
organization_staff_service = OrganizationStaffService(db)

@strawberry.type
class OrganizationStaffQuery:

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_organization_staff(self, org_staff_id: str) -> OrganizationStaffType:
        organization_staff = await organization_staff_service.get_organization_staff(org_staff_id)
        if not organization_staff:
            raise NotFoundException("Organization Staff not found")
        return OrganizationStaffType.from_orm(organization_staff)

    
    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_org_staffs_by_user_id(self, user_id: str) -> list[OrganizationStaffType]:
        organization_staffs = await organization_staff_service.get_organization_by_user_id(user_id)
        if not organization_staffs:
            raise NotFoundException("Organization Staff not found")
        return [await OrganizationStaffType.from_orm(db, organization_staff) for organization_staff in organization_staffs]
