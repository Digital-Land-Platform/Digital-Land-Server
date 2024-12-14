import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .service import PropertyCatagoryService
from .types import PropertyCatagoryType, PropertyCatagoryInput, UpdatePropertyCatagory
from config.database import db
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole


auth_management = AuthManagement()
catagory_service = PropertyCatagoryService(db)

@strawberry.type
class PropertyCatagoryMutation:

    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def create_property_catagory(self, info, catagory: PropertyCatagoryInput) -> PropertyCatagoryType:
        catagory = vars(catagory)
        catagory_data = await catagory_service.create_catagory(catagory)
        return PropertyCatagoryType.from_orm(catagory_data)
    
    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def update_property_catagory(self, info, catagory_id: str, catagory_data: UpdatePropertyCatagory) -> PropertyCatagoryType:
        catagory_data = vars(catagory_data)
        catagory = await catagory_service.update_catagory(catagory_id, catagory_data)
        return PropertyCatagoryType.from_orm(catagory)
    
    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def delete_property_catagory(self, info, catagory_id: str) -> str:
        return await catagory_service.delete_catagory(catagory_id)
