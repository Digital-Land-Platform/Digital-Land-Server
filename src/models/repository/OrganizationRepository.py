from src.models.Organization import Organization
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class OrganizationRepository:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_organization(self, organization_data: Organization) -> Organization:
        async with self.db:
            async with self.db.session as session:
                session.add(organization_data)
                await session.commit()
                await session.refresh(organization_data)
                return organization_data

    async def update_organization(self, org_id: str, org_data: dict) -> Organization:
        async with self.db:
            async with self.db.session as session:
                organization = await session.get(Organization, org_id)
                if not organization:
                    raise Exception("Organization not found")
                for key, value in org_data.items():
                    if value and hasattr(organization, key):
                        setattr(organization, key, value)
                session.add(organization)
                await session.commit()
                await session.refresh(organization)
                return organization

    async def delete_organization(self, org_id: str) -> str:
        async with self.db:
            async with self.db.session as session:
                organization = await session.get(Organization, org_id)
                if not organization:
                    raise Exception("Organization not found")
                await session.delete(organization)
                await session.commit()
                return f"Organization with ID {org_id} deleted"

    async def get_organization(self, org_id: str) -> Organization:
        async with self.db:
            async with self.db.session as session:
                organization = await session.get(Organization, org_id)
                if not organization:
                    raise Exception("Organization not found")
                return organization

    async def get_organizations(self) -> list[Organization]:
        async with self.db:
            async with self.db.session as session:
                statement = select(Organization)
                result = await session.execute(statement)
                organizations = result.scalars().all()
                return organizations

    async def get_organization_by_name(self, org_name: str) -> Organization:
        async with self.db:
            async with self.db.session as session:
                statement = select(Organization).where(Organization.name == org_name)
                result = await session.execute(statement)
                organization = result.scalar_one_or_none()
                return organization

    async def get_organization_by_TIN(self, org_TIN: str) -> Organization:
        async with self.db:
            async with self.db.session as session:
                statement = select(Organization).where(Organization.TIN == org_TIN)
                result = await session.execute(statement)
                organization = result.scalar_one_or_none()
                return organization

