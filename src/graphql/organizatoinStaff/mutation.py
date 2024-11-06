import strawberry
from .types import OrganizationStaffType, OrganizationStaffInput
from .services import OrganizationStaffService
from src.models.enums.OrganizationRole import OrganizationRole
from config.database import db

organization_staff_service = OrganizationStaffService(db)

@strawberry.type
class OrganizationStaffMutation:

    @strawberry.mutation
    async def create_organization_staff(self, organization_staff_data: OrganizationStaffInput) -> OrganizationStaffType:
        try:
            
            organization_staff_data = vars(organization_staff_data)
            organization_staff = await organization_staff_service.create_organization_staff(organization_staff_data)
            if not organization_staff:
                raise Exception("Failed to create Organization Staff")
            return await OrganizationStaffType.from_orm(db, organization_staff)
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to create Organization Staff: {e}")

    @strawberry.mutation
    async def update_organization_staff(self, org_staff_id: str, org_staff_data: OrganizationStaffInput) -> OrganizationStaffType:
        try:
            org_staff_data = vars(org_staff_data)
            organization_staff = await organization_staff_service.update_organization_staff(org_staff_id, org_staff_data)
            if not organization_staff:
                raise Exception("Failed to update Organization Staff")
            return await OrganizationStaffType.from_orm(db, organization_staff)
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to update Organization Staff: {e}")

    @strawberry.mutation
    async def delete_organization_staff(self, org_id: str) -> str:
        try:
            message = await organization_staff_service.delete_organization_staff(org_id)
            return message
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to delete Organization Staff: {e}")