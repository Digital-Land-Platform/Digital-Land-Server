from typing import Dict
from src.models.OrganizationProfile import OrganizationProfile
from src.models.repository.OrganizationProfileRepository import OrganizationProfileRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException,
    NotFoundException,
    InternalServerErrorException,
    CustomException,
)


class OrganizationProfileService:
        
        def __init__(self, db: AsyncSession):
            self.db = db
            self.organization_profile_repo = OrganizationProfileRepository(db)
        
        async def create_organization_profile(self, organization_data: Dict) -> OrganizationProfile:
            try:
                check_website = await self.organization_profile_repo.get_organization_profile_by_website_url(organization_data.get("website_url"))
                if check_website:
                    raise CustomException(status_code=409, detail="Organization with website already exists")
                org_profile = OrganizationProfile(**organization_data)
                return await self.organization_profile_repo.create_organization_profile(org_profile)
            except CustomException as e:
                raise e
            except Exception as e:
                raise InternalServerErrorException()
        
        async def update_organization_profile(self, org_id: str, org_data: dict) -> OrganizationProfile:
            try:
                org = await self.organization_repo.get_organization(org_id)
                if not org:
                    raise NotFoundException("Organization not found")
            
                return await self.organization_profile_repo.update_organization_profile(org_id, org_data)
            except NotFoundException as e:
                raise e
            except Exception as e:
                raise InternalServerErrorException()
        
        async def delete_organization_profile(self, org_id: str) -> str:
            try:
                org = await self.organization_repo.get_organization(org_id)
                if not org:
                    raise NotFoundException("Organization not found")
                
                return await self.organization_profile_repo.delete_organization_profile(org_id)
            except NotFoundException as e:
                raise e
            except Exception as e:
                raise InternalServerErrorException()
        
        async def get_organization_profile(self, org_id: str) -> OrganizationProfile:
            try:
                org = await self.organization_repo.get_organization(org_id)
                if not org:
                    raise NotFoundException("Organization not found")
                
                return await self.organization_profile_repo.get_organization_profile(org_id)
            except NotFoundException as e:
                raise e
            except Exception as e:
                raise InternalServerErrorException()
        
        async def get_all_organization_profiles(self) -> list[OrganizationProfile]:
            try:
                return await self.organization_profile_repo.get_organization_profiles()
            except Exception as e:
                raise InternalServerErrorException()
            