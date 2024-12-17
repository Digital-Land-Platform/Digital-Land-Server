import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .services import PropertyCatagoryRelationService
from .types import PropertyCatagoryRelationshipType
from .types import PropertyCatagoryRelationshipInput, UpdatePropertyCatagoryRelationship
from config.database import db
from src.middleware.AuthManagment import AuthManagement

auth_management = AuthManagement()
catagory_relationship_service = PropertyCatagoryRelationService(db)

@strawberry.type
class PropertyCatagoryRelationshipMutation:

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def create_catagory_relationship(self, catagory_relationship: PropertyCatagoryRelationshipInput) -> PropertyCatagoryRelationshipType:
        catagory_relationship = vars(catagory_relationship)
        catagory_relationship_data = await catagory_relationship_service.create_relation(catagory_relationship)
        return PropertyCatagoryRelationshipType.from_orm(catagory_relationship_data)
    
    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def update_catagory_relationship(self, catagory_relationship_id: str, catagory_relationship_data: UpdatePropertyCatagoryRelationship) -> PropertyCatagoryRelationshipType:
        catagory_relationship_data = vars(catagory_relationship_data)
        catagory_relationship = await catagory_relationship_service.update_relation(catagory_relationship_id, catagory_relationship_data)
        return PropertyCatagoryRelationshipType.from_orm(catagory_relationship)
    
    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def delete_catagory_relationship(self, catagory_relationship_id: str) -> str:
        return await catagory_relationship_service.delete_relation(catagory_relationship_id)
