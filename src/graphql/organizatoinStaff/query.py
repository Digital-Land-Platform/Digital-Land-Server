import strawberry
from config.database import db
from .types import OrganizationStaffType, OrganizationStaffInput
from .services import OrganizationStaffService

organization_staff_service = OrganizationStaffService(db)

@strawberry.type
class OrganizationStaffQuery:

    @strawberry.field
    async def get_organization_staff(self, org_staff_id: str) -> OrganizationStaffType:
        try:
            organization_staff = await organization_staff_service.get_organization_staff(org_staff_id)
            if not organization_staff:
                raise Exception("Organization Staff not found")
            return OrganizationStaffType.from_orm(organization_staff)
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to get Organization Staff: {e}")
    
    @strawberry.field
    async def get_org_staffs_by_user_id(self, user_id: str) -> list[OrganizationStaffType]:
        try:
            organization_staffs = await organization_staff_service.get_organization_by_user_id(user_id)
            return [await OrganizationStaffType.from_orm(db, organization_staff) for organization_staff in organization_staffs]
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to get Organization Staffs: {e}")
