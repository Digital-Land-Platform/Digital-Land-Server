from sqlalchemy.ext.asyncio import AsyncSession
from src.models.Reel import Reel
from sqlalchemy.future import select
from uuid import UUID
from sqlalchemy.orm import selectinload

class ReelRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_reel(self, reel: Reel) -> Reel:
        self.db.add(reel)
        await self.db.commit()
        await self.db.refresh(reel)
        return reel

    async def get_reels_by_property(self, property_id: UUID) -> list[Reel]:
        async with self.db as session:
            # Query to fetch all reels associated with the given property_id
            result = await session.execute(
                select(Reel).filter(Reel.property_id == property_id)
            )
            return result.scalars().all()

    async def get_reel_by_id(self, reel_id: UUID) -> Reel:
        query = select(Reel).where(Reel.id == reel_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def update_reel(self, reel: Reel) -> Reel:
        await self.db.commit()
        await self.db.refresh(reel)
        return reel

    async def delete_reel(self, reel: Reel) -> None:
        await self.db.delete(reel)
        await self.db.commit()

    async def check_reel_limit(self, property_id: UUID) -> bool:
        query = select(Reel).where(Reel.property_id == property_id)
        result = await self.db.execute(query)
        reels = result.scalars().all()
        return len(reels) < 3  # Assuming the max limit is 3
