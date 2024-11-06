from src.models.enums.OrganizationRole import OrganizationRole
from src.models.repository.OrganizationStaffRepository import OrganizationStaffRepository
from src.models.repository.OrganizationRepository import OrganizationRepository
from src.models.repository.UserProfileRepository import UserProfileRepository   
from src.models.OrganizationStaff import OrganizationStaff
from sqlalchemy.ext.asyncio import AsyncSession
from src.middleware.UserProfileValidator import UserProfileValidator
from config.database import db

class OrganizationStaffService:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.organization_staff_repo = OrganizationStaffRepository(db)
        self.user_profile_repo = UserProfileRepository(db)
        self.organization_repo  = OrganizationRepository(db)
    
    async def create_organization_staff(self, organization_staff_data: dict) -> OrganizationStaff:
        try:
            if "role" in organization_staff_data and organization_staff_data["role"]:
            # Get the name from the Strawberry enum
                role_name = organization_staff_data["role"].name

                # Use getattr to safely access the enum by name
                organization_staff_data["role"] = getattr(OrganizationRole, role_name, None)
                if organization_staff_data["role"] is None:
                    raise ValueError(f"Invalid role: {role_name}")
            if not await self.user_profile_repo.get_user_profile_by_id(organization_staff_data.get("user_id")):
                raise Exception("User not found")
            if not await self.organization_repo.get_organization(organization_staff_data.get("organization_id")):
                raise Exception("Organization not found")
            organization_staff_data["start_date"] = UserProfileValidator.change_str_date(organization_staff_data.get("start_date"), "start_date")
            if organization_staff_data["end_date"]:
                organization_staff_data["end_date"] = UserProfileValidator.change_str_date(organization_staff_data.get("end_date"), "end_date")
            else:
                organization_staff_data.pop("end_date")
            return await self.organization_staff_repo.create_organization_staff(OrganizationStaff(**organization_staff_data))
        except Exception as e:
            raise Exception(f"Failed to create organization staff: {e}")
    
    async def update_organization_staff(self, main_id: str, updated_staff: dict) -> OrganizationStaff:
        try:
            if "role" in updated_staff and updated_staff["role"]:
            # Get the name from the Strawberry enum
                role_name = updated_staff["role"].name

                # Use getattr to safely access the enum by name
                updated_staff["role"] = getattr(OrganizationRole, role_name, None)
                if updated_staff["role"] is None:
                    raise ValueError(f"Invalid role: {role_name}")
            if not await self.user_profile_repo.get_user_profile_by_id(updated_staff.get("user_id")):
                raise Exception("User not found")
            if not await self.organization_repo.get_organization(updated_staff.get("organization_id")):
                raise Exception("Organization not found")
            if updated_staff["start_date"]:
                updated_staff["start_date"] = UserProfileValidator.change_str_date(updated_staff.get("start_date"), "start_date")
            if updated_staff["end_date"]:
                updated_staff["end_date"] = UserProfileValidator.change_str_date(updated_staff.get("end_date"), "end_date")
            else:
                updated_staff.pop("end_date")
            return await self.organization_staff_repo.update_organization_staff(main_id, updated_staff)
        except Exception as e:
            raise Exception(f"Failed to update staff: {e}")
    
    async def delete_organization_staff(self, main_id: str) -> str:
        try:
            return await self.organization_staff_repo.delete_organization_staff(main_id)
        except Exception as e:
            raise Exception(f"Failed to delete staff: {e}")
    
    async def get_organization_staff_by_id(self, main_id: str) -> OrganizationStaff:
        try:
            return await self.organization_staff_repo.get_organization_staff_by_id(main_id)
        except Exception as e:
            raise Exception(f"Failed to get staff: {e}")
    
    async def get_organization_by_user_id(self, user_id: str) -> list[OrganizationStaff]:
        try:
            return await self.organization_staff_repo.get_organization_by_user_id(user_id)
        except Exception as e:
            raise Exception(f"Failed to get organization by user ID: {e}")