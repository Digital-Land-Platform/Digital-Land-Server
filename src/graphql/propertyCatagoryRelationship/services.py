from typing import List
from src.models.repository.PropertyCatagoryRelationshipRepository import PropertyCatagoryRelationRepository
from src.models.PropertyCatagoryRelation import PropertyCatagoryRelation


class PropertyCatagoryRelationService:

    def __init__(self, db):
        self.db = db
        self.relation_repo = PropertyCatagoryRelationRepository(self.db)

    async def create_relation(self, relation: dict) -> PropertyCatagoryRelation:
        try:
            return await self.relation_repo.create_relation(PropertyCatagoryRelation(**relation))
        except Exception as e:
            raise Exception(f"Error creating relation: {e}")
    
    async def update_relation(self, relation_id: str, relation_data: dict) -> PropertyCatagoryRelation:
        try:
            return await self.relation_repo.update_relation(relation_id, relation_data)
        except Exception as e:
            raise Exception(f"Error updating relation: {e}")
    
    async def get_relation(self, relation_id: str) -> PropertyCatagoryRelation:
        try:
            return await self.relation_repo.get_relation(relation_id)
        except Exception as e:
            raise Exception(f"Error getting relation: {e}")
    
    async def get_relation_by_property_id(self, property_id: str) -> List[PropertyCatagoryRelation]:
        try:
            return await self.relation_repo.get_relation_by_property_id(property_id)
        except Exception as e:
            raise Exception(f"Error getting relation: {e}")
    
    async def get_relation_by_catagory_id(self, catagory_id: str) -> PropertyCatagoryRelation:
        try:
            return await self.relation_repo.get_relation_by_catagory_id(catagory_id)
        except Exception as e:
            raise Exception(f"Error getting relation: {e}")
    
    async def delete_relation(self, relation_id: str) -> str:
        try:
            return await self.relation_repo.delete_relation(relation_id)
        except Exception as e:
            raise Exception(f"Error deleting relation: {e}")