from typing import List
import strawberry
from .services import PropertyCatagoryRelationService
from .types import PropertyCatagoryRelationshipType
from config.database import db

catagory_relationship_service = PropertyCatagoryRelationService(db)

@strawberry.type
class PropertyCatagoryRelationshipQuery:

    @strawberry.field
    async def get_relation_by_catagory_id(self, catagory_id: str) -> PropertyCatagoryRelationshipType:
        try:
            catagory = await catagory_relationship_service.get_relation_by_catagory_id(catagory_id)
            return PropertyCatagoryRelationshipType.from_orm(catagory)
        except Exception as e:
            raise Exception(f"Error fetching catagory relationship: {e}")
    
    @strawberry.field
    async def get_relation_by_property_id(self, property_id: str) -> List[PropertyCatagoryRelationshipType]:
        try:
            catagories = await catagory_relationship_service.get_relation_by_property_id(property_id)
            return [PropertyCatagoryRelationshipType.from_orm(catagory) for catagory in catagories]
        except Exception as e:
            raise Exception(f"Error fetching catagory relationship: {e}")