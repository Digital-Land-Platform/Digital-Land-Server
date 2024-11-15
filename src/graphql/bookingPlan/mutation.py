import strawberry
from .services import BookingPlanService
from .types import BookingPlanType, BookingPlanInput, UpdateBookingPlanInput
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole
from config.database import db


auth_manager = AuthManagement()
booking_plan_service = BookingPlanService(db)


@strawberry.type
class BookingPlanMutation:

    @strawberry.mutation
    @auth_manager.role_required([UserRole.ADMIN, UserRole.NOTARY])
    async def create_booking_plan(self, info, booking_plan_data: BookingPlanInput) -> BookingPlanType:
        try:
            booking_plan_data = vars(booking_plan_data)
            value = await booking_plan_service.create_booking_plan(booking_plan_data)
            return BookingPlanType.from_orm(value)
        except Exception as e:
            raise strawberry.exceptions.StrawberryGraphQLError(f"Error creating booking plan: {e}")

    @strawberry.mutation
    @auth_manager.role_required([UserRole.ADMIN, UserRole.NOTARY])
    async def update_booking_plan(self, info, booking_plan_id: str, booking_plan_data: UpdateBookingPlanInput) -> BookingPlanType:
        try:
            booking_plan_data = vars(booking_plan_data)
            value = await booking_plan_service.update_booking_plan(booking_plan_id, booking_plan_data)
            return BookingPlanType.from_orm(value)
        except Exception as e:
            raise strawberry.exceptions.StrawberryGraphQLError(f"Error creating booking plan: {e}") 

    @strawberry.mutation
    @auth_manager.role_required([UserRole.ADMIN, UserRole.NOTARY])
    async def delete_booking_plan(self, info, booking_plan_id: str) -> str:
        return await booking_plan_service.delete_booking_plan(booking_plan_id)