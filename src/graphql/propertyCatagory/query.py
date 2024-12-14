import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .service import PropertyCatagoryService
from .types import PropertyCatagoryType
from config.database import db
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole

auth_manager = AuthManagement()
catagory_service = PropertyCatagoryService(db)


@strawberry.type
class PropertyCatagoryQuery:

    @strawberry.field
    @ExceptionHandler.handle_exceptions
    async def get_property_catagory(self, info, catagory_id: str) -> PropertyCatagoryType:
        catagory = await catagory_service.get_catagory(catagory_id)
        return PropertyCatagoryType.from_orm(catagory)
    
    @strawberry.field
    @ExceptionHandler.handle_exceptions
    async def get_property_catagory_by_name(self, info, name: str) -> PropertyCatagoryType:
        catagory = await catagory_service.get_catagory_by_name(name)
        return PropertyCatagoryType.from_orm(catagory)
