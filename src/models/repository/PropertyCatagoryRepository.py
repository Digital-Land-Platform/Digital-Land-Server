from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.PropertyCatagories import PropertyCatagories


class PropertyCatagoriesRepository:

    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_catagory(self, catagory: PropertyCatagories) -> PropertyCatagories:
        try:
            async with self.db:
                async with self.db.session as session:
                    session.add(catagory)
                    await session.commit()
                    await session.refresh(catagory)
                    return catagory
        except Exception as e:
            raise Exception(f"Error creating catagory: {e}")
    
    async def update_catagory(self, catagory_id: str, catagory_data: dict) -> PropertyCatagories:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(PropertyCatagories).where(PropertyCatagories.id == catagory_id)
                    )
                    catagory = result.scalar_one_or_none()
                    for key, value in catagory_data.items():
                        if value and hasattr(catagory, key):
                            setattr(catagory, key, value)
                    session.add(catagory)
                    await session.commit()
                    await session.refresh(catagory)
                    return catagory
        except Exception as e:
            raise Exception(f"Error updating catagory: {e}")
    
    async def get_catagory(self, catagory_id: str) -> PropertyCatagories:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(PropertyCatagories).where(PropertyCatagories.id == catagory_id)
                    )
                    return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error getting catagory: {e}")
    
    async def get_catagory_by_name(self, name: str) -> PropertyCatagories:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(PropertyCatagories).where(PropertyCatagories.name == name)
                    )
                    return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error getting catagory: {e}")
    
    async def delete_catagory(self, catagory_id: str) -> str:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(PropertyCatagories).where(PropertyCatagories.id == catagory_id)
                    )
                    catagory = result.scalar_one_or_none()
                    await session.delete(catagory)
                    await session.commit()
                    return "Catagory deleted successfully"
        except Exception as e:
            raise Exception(f"Error deleting catagory: {e}")