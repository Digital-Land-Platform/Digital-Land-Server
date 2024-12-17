from typing import List
import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .services import AvailabilityService
from .types import AvailabilityType, ChooseAvailabilityInput
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole
from config.database import db


auth_management = AuthManagement()
availabity_service = AvailabilityService(db)

@strawberry.type
class AvailabilityQuery:

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_availability(self, info, availability_id: str) -> AvailabilityType:
        value = await availabity_service.get_availability(availability_id)
        return AvailabilityType.from_orm(value)

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_availability_by_status(self, info, status: ChooseAvailabilityInput) -> List[AvailabilityType]:
        values = await availabity_service.get_availability_by_status(status)
        return [AvailabilityType.from_orm(value) for value in values]
 
    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_all_availability(self, info) -> List[AvailabilityType]:
        values = await availabity_service.get_all_availability()
        return [AvailabilityType.from_orm(value) for value in values]
