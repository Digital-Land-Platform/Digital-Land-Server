from typing import List
import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .services import BookingPlanService
from .types import BookingPlanType, ChooseBookingPlanInput
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole
from config.database import db

auth_management = AuthManagement()
booking_plan_service = BookingPlanService(db)

@strawberry.type
class BookingPlanQuery:

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_booking_plan(self, info, booking_plan_id: str) -> BookingPlanType:
        value = await booking_plan_service.get_booking_plan(booking_plan_id)
        return BookingPlanType.from_orm(value)

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_all_booking_plan(self, info) -> List[BookingPlanType]:
        values = await booking_plan_service.get_all_booking_plan()
        return [BookingPlanType.from_orm(value) for value in values]

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_booking_plan_by_status(self, info, status: ChooseBookingPlanInput) -> List[BookingPlanType]:
            values = await booking_plan_service.get_booking_plan_by_status(status)
            return [BookingPlanType.from_orm(value) for value in values]
