from typing import List
import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .services import PropertyCatagoryRelationService
from .types import PropertyCatagoryRelationshipType
from config.database import db

catagory_relationship_service = PropertyCatagoryRelationService(db)

@strawberry.type
class PropertyCatagoryRelationshipQuery:

    @strawberry.field
    @ExceptionHandler.handle_exceptions
    async def get_relation_by_catagory_id(self, catagory_id: str) -> PropertyCatagoryRelationshipType:
        catagory = await catagory_relationship_service.get_relation_by_catagory_id(catagory_id)
        return PropertyCatagoryRelationshipType.from_orm(catagory)

    
    @strawberry.field
    @ExceptionHandler.handle_exceptions
    async def get_relation_by_property_id(self, property_id: str) -> List[PropertyCatagoryRelationshipType]:
        catagories = await catagory_relationship_service.get_relation_by_property_id(property_id)
        return [PropertyCatagoryRelationshipType.from_orm(catagory) for catagory in catagories]
        