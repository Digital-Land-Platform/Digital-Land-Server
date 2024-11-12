from src.models.OrganizationStaff import OrganizationStaff
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class OrganizationStaffRepository:
        
        def __init__(self, db: AsyncSession):
            self.db = db
    
        async def create_organization_staff(self, organization_staff: OrganizationStaff) -> OrganizationStaff:
            try:
                async with self.db:
                    async with self.db.session as session:
                        session.add(organization_staff)
                        await session.commit()
                        await session.refresh(organization_staff)
                        return organization_staff
            except Exception as e:
                raise Exception(f"Failed to create organization staff: {e}")
        
        async def update_organization_staff(self, main_id: str, updated_staff: dict) -> OrganizationStaff:
            try:
                async with self.db:
                    async with self.db.session as session:
                        staff = await session.get(OrganizationStaff, main_id)
                        if not staff:
                            raise Exception("Staff not found")
                        for key, value in updated_staff.items():
                            if value and hasattr(staff, key):
                                setattr(staff, key, value)
                        session.add(staff)
                        await session.commit()
                        await session.refresh(staff)
                        return staff
            except Exception as e:
                raise Exception(f"Failed to update staff: {e}")
        
        async def delete_organization_staff(self, main_id: str) -> str:
            try:
                async with self.db:
                    async with self.db.session as session:
                        staff = await session.get(OrganizationStaff, main_id)
                        if not staff:
                            raise Exception("Staff not found")
                        await session.delete(staff)
                        await session.commit()
                        return f"Staff {main_id} deleted"
            except Exception as e:
                raise Exception(f"Failed to delete staff: {e}")
        
        async def get_organization_staff_by_id(self, main_id: str) -> OrganizationStaff:
            try:
                async with self.db:
                    async with self.db.session as session:
                        staff = await session.get(OrganizationStaff, main_id)
                        if not staff:
                            raise Exception("Staff not found")
                        return staff
            except Exception as e:
                raise Exception(f"Failed to get staff: {e}")

        async def get_organization_by_user_id(self, user_id: str) -> list[OrganizationStaff]:
            try:
                async with self.db:
                    async with self.db.session as session:
                        stmt = select(OrganizationStaff).filter(OrganizationStaff.user_id == user_id)
                        result = await session.execute(stmt)
                        staff = result.scalars().all()
                        if not staff:
                            raise Exception("Staff not found")
                        return staff
            except Exception as e:
                raise Exception(f"Failed to get staff: {e}")