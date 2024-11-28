import strawberry
from .service import PropertyCatagoryService
from .types import PropertyCatagoryType, PropertyCatagoryInput, UpdatePropertyCatagory
from config.database import db
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole


auth_manager = AuthManagement()
catagory_service = PropertyCatagoryService(db)

@strawberry.type
class PropertyCatagoryMutation:

    @strawberry.mutation
    @auth_manager.role_required([UserRole.ADMIN])
    async def create_property_catagory(self, info, catagory: PropertyCatagoryInput) -> PropertyCatagoryType:
        try:
            catagory = vars(catagory)
            catagory_data = await catagory_service.create_catagory(catagory)
            return PropertyCatagoryType.from_orm(catagory_data)
        except Exception as e:
            raise Exception(f"Error creating catagory: {e}")
    
    @strawberry.mutation
    @auth_manager.role_required([UserRole.ADMIN])
    async def update_property_catagory(self, info, catagory_id: str, catagory_data: UpdatePropertyCatagory) -> PropertyCatagoryType:
        try:
            catagory_data = vars(catagory_data)
            catagory = await catagory_service.update_catagory(catagory_id, catagory_data)
            return PropertyCatagoryType.from_orm(catagory)
        except Exception as e:
            raise Exception(f"Error updating catagory: {e}")
    
    @strawberry.mutation
    @auth_manager.role_required([UserRole.ADMIN])
    async def delete_property_catagory(self, info, catagory_id: str) -> str:
        try:
            return await catagory_service.delete_catagory(catagory_id)
        except Exception as e:
            raise Exception(f"Error deleting catagory: {e}")