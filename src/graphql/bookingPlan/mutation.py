import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .services import BookingPlanService
from .types import BookingPlanType, BookingPlanInput, UpdateBookingPlanInput
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole
from config.database import db


auth_management = AuthManagement()
booking_plan_service = BookingPlanService(db)


@strawberry.type
class BookingPlanMutation:

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def create_booking_plan(self, info, booking_plan_data: BookingPlanInput) -> BookingPlanType:
        booking_plan_data = vars(booking_plan_data)
        value = await booking_plan_service.create_booking_plan(booking_plan_data)
        return BookingPlanType.from_orm(value)

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def update_booking_plan(self, info, booking_plan_id: str, booking_plan_data: UpdateBookingPlanInput) -> BookingPlanType:
        booking_plan_data = vars(booking_plan_data)
        value = await booking_plan_service.update_booking_plan(booking_plan_id, booking_plan_data)
        return BookingPlanType.from_orm(value)

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def delete_booking_plan(self, info, booking_plan_id: str) -> str:
        return await booking_plan_service.delete_booking_plan(booking_plan_id)