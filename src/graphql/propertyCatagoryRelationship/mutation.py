import strawberry
from .services import PropertyCatagoryRelationService
from .types import PropertyCatagoryRelationshipType
from .types import PropertyCatagoryRelationshipInput, UpdatePropertyCatagoryRelationship
from config.database import db

catagory_relationship_service = PropertyCatagoryRelationService(db)

@strawberry.type
class PropertyCatagoryRelationshipMutation:

    @strawberry.mutation
    async def create_catagory_relationship(self, catagory_relationship: PropertyCatagoryRelationshipInput) -> PropertyCatagoryRelationshipType:
        try:
            catagory_relationship = vars(catagory_relationship)
            catagory_relationship_data = await catagory_relationship_service.create_relation(catagory_relationship)
            return PropertyCatagoryRelationshipType.from_orm(catagory_relationship_data)
        except Exception as e:
            raise Exception(f"Error creating catagory relationship: {e}")
    
    @strawberry.mutation
    async def update_catagory_relationship(self, catagory_relationship_id: str, catagory_relationship_data: UpdatePropertyCatagoryRelationship) -> PropertyCatagoryRelationshipType:
        try:
            catagory_relationship_data = vars(catagory_relationship_data)
            catagory_relationship = await catagory_relationship_service.update_relation(catagory_relationship_id, catagory_relationship_data)
            return PropertyCatagoryRelationshipType.from_orm(catagory_relationship)
        except Exception as e:
            raise Exception(f"Error updating catagory relationship: {e}")
    
    @strawberry.mutation
    async def delete_catagory_relationship(self, catagory_relationship_id: str) -> str:
        try:
            return await catagory_relationship_service.delete_relation(catagory_relationship_id)
        except Exception as e:
            raise Exception(f"Error deleting catagory relationship: {e}")