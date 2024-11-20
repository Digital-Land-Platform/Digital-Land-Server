from typing import List
import strawberry
from .services import AvailabilityService
from .types import AvailabilityType, ChooseAvailabilityInput
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole
from config.database import db


auth_manager = AuthManagement()
availabity_service = AvailabilityService(db)

@strawberry.type
class AvailabilityQuery:

    @strawberry.field
    @auth_manager.role_required([UserRole.ADMIN, UserRole.NOTARY])
    async def get_availability(self, info, availability_id: str) -> AvailabilityType:
        try:
            value = await availabity_service.get_availability(availability_id)
            return AvailabilityType.from_orm(value)
        except Exception as e:
            raise strawberry.exceptions.StrawberryGraphQLError(f"Error getting availability: {e}")
    @strawberry.field
    @auth_manager.role_required([UserRole.ADMIN, UserRole.NOTARY])
    async def get_availability_by_status(self, info, status: ChooseAvailabilityInput) -> List[AvailabilityType]:
        try:
            values = await availabity_service.get_availability_by_status(status)
            return [AvailabilityType.from_orm(value) for value in values]
        except Exception as e:
            raise strawberry.exceptions.StrawberryGraphQLError(f"Error getting availability by status: {e}")
    
    @strawberry.field
    @auth_manager.role_required([UserRole.ADMIN, UserRole.NOTARY])
    async def get_all_availability(self, info) -> List[AvailabilityType]:
        try:
            values = await availabity_service.get_all_availability()
            return [AvailabilityType.from_orm(value) for value in values]
        except Exception as e:
            raise strawberry.exceptions.StrawberryGraphQLError(f"Error getting all availability: {e}")