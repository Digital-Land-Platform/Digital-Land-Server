import strawberry
import strawberry.exceptions

from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .services import AvailabilityService
from .types import AvailabilityType, AvailabilityInput, UpdateAvailabiltyInput
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole
from config.database import db


auth_management = AuthManagement()
availabity_service = AvailabilityService(db)

@strawberry.type
class AvailabilityMutation:

    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required(UserRole.NOTARY)
    @ExceptionHandler.handle_exceptions
    async def create_availability(self, info, availability_data: AvailabilityInput) -> AvailabilityType:
        availability_data = vars(availability_data)
        value = await availabity_service.create_availability(availability_data)
        return AvailabilityType.from_orm(value)
        
    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required(UserRole.NOTARY)
    @ExceptionHandler.handle_exceptions
    async def update_availability(self, info, availability_id: str, availability_data: UpdateAvailabiltyInput) -> AvailabilityType:
        availability_data = vars(availability_data)
        value = await availabity_service.update_availability(availability_id, availability_data)
        return AvailabilityType.from_orm(value)

    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required(UserRole.NOTARY)
    @ExceptionHandler.handle_exceptions
    async def delete_availability(self, info, availability_id: str) -> str:
        return await availabity_service.delete_availability(availability_id)
