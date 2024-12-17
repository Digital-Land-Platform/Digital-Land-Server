from datetime import datetime
from src.models.Organization import Organization
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.repository.OrganizationRepository import OrganizationRepository
from src.middleware.UserProfileValidator import UserProfileValidator
from src.graphql.users.services import UserService
from src.graphql.organizatoinStaff.services import OrganizationStaffService
from src.graphql.userProfile.service import UserProfileService
from src.models.OrganizationStaff import OrganizationStaff
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    # BadRequestException,
    NotFoundException,
    InternalServerErrorException,
    CustomException,
)

class OrganizationService:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.organization_repo = OrganizationRepository(self.db)
        self.user_service = UserService(self.db)
        self.org_staff_service = OrganizationStaffService(self.db)
        self.user_profile_service = UserProfileService(self.db)
    
    async def create_organization(self, organization_data: dict, user_email) -> OrganizationStaff:
        try:
            if await self.organization_repo.get_organization_by_TIN(organization_data.get("TIN")):
                raise CustomException(status_code=409, detail="Organization with TIN already exists")
            
            if await self.organization_repo.get_organization_by_name(organization_data.get("name")):
                raise CustomException(status_code=409, detail="Organization with name already exists")
            
            user = await self.user_service.get_user_by_email(user_email)
            if not user:
                raise NotFoundException("User not found")
            
            user_profile = await self.user_profile_service.get_user_profile_by_user_id(str(user.id))
            if not user_profile:
                raise NotFoundException("User profile not found")
            
            organization_staff = {
                "organization_id": organization_data.pop("organization_id"),
                "user_id": str(user_profile.id),
                "role": organization_data.pop("role"),
                "start_date": organization_data.pop("start_date"),
                "end_date": organization_data.pop("end_date"),
            }

            organization_data.pop("user_id")
            if organization_data["issue_date"]:
                organization_data["issue_date"] = UserProfileValidator.change_str_date(organization_data.get("issue_date"), "issue_date")
            if organization_data.get("expiration_date"):
                organization_data["expiration_date"] = UserProfileValidator.change_str_date(organization_data.get("expiration_date"), "expiration_date")  
            else:
                organization_data.pop("expiration_date")

            organization_data["verification_date"] = datetime.now()
            organization = Organization(**organization_data)
            org = await self.organization_repo.create_organization(organization)
            organization_staff["organization_id"] = str(org.id)

            await self.org_staff_service.create_organization_staff(organization_staff)
            return org
        except (CustomException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def update_organization(self, org_id: str, org_data: dict) -> Organization:
        try:
            org = await self.organization_repo.get_organization(org_id)
            if not org:
                raise NotFoundException("Organization not found")
            
            prev_tin_number = await self.organization_repo.get_organization_by_TIN(org_data.get("TIN"))
            if prev_tin_number and str(prev_tin_number.id) != org_id:
                raise CustomException(status_code=409, detail="Organization with TIN already exists")
            
            prev_name = await self.organization_repo.get_organization_by_name(org_data.get("name"))
            if prev_name and str(prev_name.id) != org_id:
                CustomException(status_code=409, detail="Organization with name already exists")

            org_data.pop("role"),
            org_data.pop("start_date"),
            org_data.pop("end_date"),
            org_data.pop("user_id")
            org_data.pop("organization_id")
            return await self.organization_repo.update_organization(org_id, org_data)
        except (CustomException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def delete_organization(self, org_id: str) -> str:
        try:
            org = await self.organization_repo.get_organization(org_id)
            if not org:
                raise NotFoundException("Organization not found")
        
            return await self.organization_repo.delete_organization(org_id)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_organization(self, org_id: str) -> Organization:
        try:
            org = await self.organization_repo.get_organization(org_id)
            if not org:
                raise NotFoundException("Organization not found")
            return org
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_all_organizations(self) -> list[Organization]:
        try:
            return await self.organization_repo.get_organizations()
        except Exception as e:
            raise InternalServerErrorException()