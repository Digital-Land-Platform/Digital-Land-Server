from typing import List
from src.models.repository.PropertyCatagoryRelationshipRepository import PropertyCatagoryRelationRepository
from src.models.PropertyCatagoryRelation import PropertyCatagoryRelation
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    InternalServerErrorException, NotFoundException
)

class PropertyCatagoryRelationService:

    def __init__(self, db):
        self.db = db
        self.relation_repo = PropertyCatagoryRelationRepository(self.db)

    async def create_relation(self, relation: dict) -> PropertyCatagoryRelation:
        try:
            return await self.relation_repo.create_relation(PropertyCatagoryRelation(**relation))
        except Exception as e:
            raise InternalServerErrorException()
    
    async def update_relation(self, relation_id: str, relation_data: dict) -> PropertyCatagoryRelation:
        try:
            relationship = self.relation_repo.get_relation(relation_id)
            if not relationship:
                raise NotFoundException(detail="Relation not found")
            
            return await self.relation_repo.update_relation(relation_id, relation_data)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_relation(self, relation_id: str) -> PropertyCatagoryRelation:
        try:
            relationship = self.relation_repo.get_relation(relation_id)
            if not relationship:
                raise NotFoundException(detail="Relationship not found")
            
            return relationship
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_relation_by_property_id(self, property_id: str) -> List[PropertyCatagoryRelation]:
        try:
            # This is needed to be fixed, It should be checking if the property exists and it is in a list of PropertyCatagoryRelation
            return await self.relation_repo.get_relation_by_property_id(property_id)
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_relation_by_catagory_id(self, catagory_id: str) -> PropertyCatagoryRelation:
        try:
            # This is a bug, it should return a list of PropertyCatagoryRelation
            # Also, it should be checking if the catagory exists
            return await self.relation_repo.get_relation_by_catagory_id(catagory_id)
        except Exception as e:
            raise InternalServerErrorException()
    
    async def delete_relation(self, relation_id: str) -> str:
        try:
            # It should be checking if the catagory exists first
            return await self.relation_repo.delete_relation(relation_id)
        except Exception as e:
            raise InternalServerErrorException()