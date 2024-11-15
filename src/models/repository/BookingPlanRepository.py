from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List
from src.models.BookingPlan import BookingPlan

class BookingPlanRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_booking_plan(self, new_booking_plan: BookingPlan) -> BookingPlan:
        try:
            async with self.db:
                async with self.db.session as session:
                    session.add(new_booking_plan)
                    await session.commit()
                    await session.refresh(new_booking_plan)
                    return new_booking_plan
        except Exception as e:
            raise Exception(f"Error creating booking plan: {e}")
        
    async def update_booking_plan(self, booking_plan_id: str, booking_plan_data: Dict) -> BookingPlan:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(BookingPlan).where(BookingPlan.id == booking_plan_id)
                    )
                    booking_plan = result.scalar_one_or_none()
                    for key, value in booking_plan_data.items():
                        if value and hasattr(booking_plan, key):
                            setattr(booking_plan, key, value)
                    session.add(booking_plan)
                    await session.commit()
                    await session.refresh(booking_plan)
                    return booking_plan
        except Exception as e:
            raise Exception(f"Error updating booking plan: {e}")
    
    async def get_booking_plan(self, booking_plan_id: str) -> BookingPlan:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(BookingPlan).where(BookingPlan.id == booking_plan_id)
                    )
                    return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error getting booking plan: {e}")
    
    async def delete_booking_plan(self, booking_plan_id: str) -> str:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(BookingPlan).where(BookingPlan.id == booking_plan_id)
                    )
                    booking_plan = result.scalar_one_or_none()
                    await session.delete(booking_plan)
                    await session.commit()
        except Exception as e:
            raise Exception(f"Error deleting booking plan: {e}")
    
    async def get_all_booking_plan(self) -> List[BookingPlan]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(BookingPlan)
                    )
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error getting all booking plan: {e}")
        
    async def get_booking_plan_by_status(self, status: str) -> List[BookingPlan]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(BookingPlan).where(BookingPlan.status == status)
                    )
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error getting booking plan by status: {e}")
    
    async def check_start_end_date(self, notary_id: str, transaction_id: str, start_time: str, end_time: str) -> BookingPlan:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(BookingPlan).filter(BookingPlan.natory_id == notary_id,
                                                    BookingPlan.transaction_id == transaction_id,
                                                   BookingPlan.start_time == start_time,
                                                   BookingPlan.end_time == end_time)
                    )
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error checking start and end date: {e}")
        