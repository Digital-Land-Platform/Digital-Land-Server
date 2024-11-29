from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.PropertyCatagories import PropertyCatagories
from src.models.repository.PropertyCatagoryRepository import PropertyCatagoriesRepository
from src.graphql.propertyCatagoryRelationship.services import PropertyCatagoryRelationService

class PropertyCatagoryService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.catagory_repo = PropertyCatagoriesRepository(self.db)
        self.property_service = PropertyCatagoryRelationService(self.db)
    
    async def create_catagory(self, catagory: Dict) -> PropertyCatagories:
        try:
            if await self.get_catagory_by_name(catagory.get("name")):
                raise Exception("Catagory already exists")
            return await self.catagory_repo.create_catagory(PropertyCatagories(**catagory))
        except Exception as e:
            raise Exception(f"Error creating catagory: {e}")
    
    async def update_catagory(self, catagory_id: str, catagory_data: Dict) -> PropertyCatagories:
        try:
            if await self.get_catagory_by_name(catagory_data.get("name")):
                raise Exception("Catagory already exists, Cancel the update")
            return await self.catagory_repo.update_catagory(catagory_id, catagory_data)
        except Exception as e:
            raise Exception(f"Error updating catagory: {e}")
    
    async def get_catagory(self, catagory_id: str) -> PropertyCatagories:
        try:
            return await self.catagory_repo.get_catagory(catagory_id)
        except Exception as e:
            raise Exception(f"Error fetching catagory: {e}")
    
    async def get_catagory_by_name(self, name: str) -> PropertyCatagories:
        try:
            return await self.catagory_repo.get_catagory_by_name(name)
        except Exception as e:
            raise Exception(f"Error fetching catagory: {e}")
    
    async def delete_catagory(self, catagory_id: str) -> str:
        try:
            catagory_relation = await self.property_service.get_relation_by_catagory_id(catagory_id)
            if catagory_relation:
                raise Exception("Catagory has a relationship with a property, Cannot delete")
            return await self.catagory_repo.delete_catagory(catagory_id)
        except Exception as e:
            raise Exception(f"Error deleting catagory: {e}")