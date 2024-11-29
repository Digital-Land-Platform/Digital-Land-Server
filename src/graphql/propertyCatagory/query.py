import strawberry
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
    @auth_manager.role_required([UserRole.ADMIN])
    async def get_property_catagory(self, info, catagory_id: str) -> PropertyCatagoryType:
        try:
            catagory = await catagory_service.get_catagory(catagory_id)
            return PropertyCatagoryType.from_orm(catagory)
        except Exception as e:
            raise Exception(f"Error fetching catagory: {e}")
    
    @strawberry.field
    @auth_manager.role_required([UserRole.ADMIN])
    async def get_property_catagory_by_name(self, info, name: str) -> PropertyCatagoryType:
        try:
            catagory = await catagory_service.get_catagory_by_name(name)
            return PropertyCatagoryType.from_orm(catagory)
        except Exception as e:
            raise Exception(f"Error fetching catagory: {e}")