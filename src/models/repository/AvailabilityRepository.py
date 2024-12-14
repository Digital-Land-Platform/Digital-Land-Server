from src.models.Availability import Availability
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List
from sqlalchemy import func, select

class AvailabilityRepository:
        
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_availability(self, new_availability: Availability) -> Availability:
        async with self.db:
            async with self.db.session as session:
                session.add(new_availability)
                await session.commit()
                await session.refresh(new_availability)
                return new_availability
            
    async def update_availability(self, availability_id: str, availability_data: Dict) -> Availability:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Availability).where(Availability.id == availability_id)
                )
                availability = result.scalar_one_or_none()
                for key, value in availability_data.items():
                    if value and hasattr(availability, key):
                        setattr(availability, key, value)
                session.add(availability)
                await session.commit()
                await session.refresh(availability)
                return availability
    
    async def get_availability(self, availability_id: str) -> Availability:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Availability).where(Availability.id == availability_id)
                )
                return result.scalar_one_or_none()
    
    async def delete_availability(self, availability_id: str) -> str:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Availability).where(Availability.id == availability_id)
                )
                availability = result.scalar_one_or_none()
                await session.delete(availability)
                await session.commit()
                return availability_id
    
    async def get_availability_by_status(self, status: str):
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Availability).filter(Availability.status == status)
                )

                availability = result.scalars().all()
                return availability
    
    async def check_start_end_date(self, notary_id: str, start_time: str, end_time: str) -> Availability:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Availability).where(
                        Availability.natory_id == notary_id,
                        func.date(Availability.start_time) == func.date(start_time),
                        func.date(Availability.end_time) == func.date(end_time)
                    )
                )

                availability = result.scalars().all()
                return availability
    
    async def get_all_availability(self) -> List[Availability]:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Availability)
                )
                return result.scalars().all()
            