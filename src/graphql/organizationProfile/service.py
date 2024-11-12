from typing import Dict
from src.models.OrganizationProfile import OrganizationProfile
from src.models.repository.OrganizationProfileRepository import OrganizationProfileRepository
from sqlalchemy.ext.asyncio import AsyncSession

class OrganizationProfileService:
        
        def __init__(self, db: AsyncSession):
            self.db = db
            self.organization_profile_repo = OrganizationProfileRepository(db)
        
        async def create_organization_profile(self, organization_data: Dict) -> OrganizationProfile:
            try:
                check_website = await self.organization_profile_repo.get_organization_profile_by_website_url(organization_data.get("website_url"))
                if check_website:
                    raise Exception("Organization with website already exists")
                org_profile = OrganizationProfile(**organization_data)
                return await self.organization_profile_repo.create_organization_profile(org_profile)
            except Exception as e:
                raise Exception(f"Failed to create Organization: {e}")
        
        async def update_organization_profile(self, org_id: str, org_data: dict) -> OrganizationProfile:
            try:
                return await self.organization_profile_repo.update_organization_profile(org_id, org_data)
            except Exception as e:
                raise Exception(f"Failed to update organization {e}")
        
        async def delete_organization_profile(self, org_id: str) -> str:
            try:
                return await self.organization_profile_repo.delete_organization_profile(org_id)
            except Exception as e:
                raise Exception(f"Failed to delete organization: {e}")
        
        async def get_organization_profile(self, org_id: str) -> OrganizationProfile:
            try:
                return await self.organization_profile_repo.get_organization_profile(org_id)
            except Exception as e:
                raise Exception(f"Failed to get Organization: {e}")
        
        async def get_all_organization_profiles(self) -> list[OrganizationProfile]:
            try:
                return await self.organization_profile_repo.get_organization_profiles()
            except Exception as e:
                raise Exception(f"Failed to get Organizations: {e}")