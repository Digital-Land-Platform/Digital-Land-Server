from src.models.OrganizationProfile import OrganizationProfile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class OrganizationProfileRepository:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def create_organization_profile(self, organization_data: OrganizationProfile) -> OrganizationProfile:
        async with self.db:
            async with self.db.session as session:
                session.add(organization_data)
                await session.commit()
                await session.refresh(organization_data)
                return organization_data
    
    async def update_organization_profile(self, org_id: str, org_data: dict) -> OrganizationProfile:
        async with self.db:
            async with self.db.session as session:
                org_profile = await session.get(OrganizationProfile, org_id)
                if not org_profile:
                    raise Exception("Organization not found")
                for key, value in org_data.items():
                    if value and hasattr(org_profile, key):
                        setattr(org_profile, key, value)
                session.add(org_profile)
                await session.commit()
                await session.refresh(org_profile)
                return org_profile
    
    async def delete_organization_profile(self, org_id: str) -> str:
        async with self.db:
            async with self.db.session as session:
                org_profile = await session.get(OrganizationProfile, org_id)
                if not org_profile:
                    raise Exception("Organization not found")
                await session.delete(org_profile)
                await session.commit()
                return f"Organization with ID {org_id} deleted"
    
    async def get_organization_profile(self, org_id: str) -> OrganizationProfile:
        async with self.db:
            async with self.db.session as session:
                org_profile = await session.get(OrganizationProfile, org_id)
                if not org_profile:
                    raise Exception("Organization not found")
                return org_profile
    
    async def get_all_organization_profiles(self) -> list[OrganizationProfile]:
        async with self.db:
            async with self.db.session as session:
                statement = select(OrganizationProfile)
                result = await session.execute(statement)
                return result.scalars().all()
    
    async def get_organization_profile_by_website_url(self, website_url: str) -> OrganizationProfile:
        async with self.db:
            async with self.db.session as session:
                statement = select(OrganizationProfile).where(OrganizationProfile.website_url == website_url)
                org_profile = await session.execute(statement)
                return org_profile.scalars().first()