from typing import List
import strawberry
from .services import BookingPlanService
from .types import BookingPlanType, ChooseBookingPlanInput
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole
from config.database import db

auth_manager = AuthManagement()
booking_plan_service = BookingPlanService(db)

@strawberry.type
class BookingPlanQuery:

    @strawberry.field
    @auth_manager.role_required([UserRole.ADMIN, UserRole.NOTARY])
    async def get_booking_plan(self, info, booking_plan_id: str) -> BookingPlanType:
        try:
            value = await booking_plan_service.get_booking_plan(booking_plan_id)
            return BookingPlanType.from_orm(value)
        except Exception as e:
            raise strawberry.exceptions.StrawberryGraphQLError(f"Error getting booking plan: {e}")
        
    @strawberry.field
    @auth_manager.role_required([UserRole.ADMIN, UserRole.NOTARY])
    async def get_all_booking_plan(self, info) -> List[BookingPlanType]:
        try:
            values = await booking_plan_service.get_all_booking_plan()
            return [BookingPlanType.from_orm(value) for value in values]
        except Exception as e:
            raise strawberry.exceptions.StrawberryGraphQLError(f"Error getting all booking plan: {e}")
    
    @strawberry.field
    @auth_manager.role_required([UserRole.ADMIN, UserRole.NOTARY])
    async def get_booking_plan_by_status(self, info, status: ChooseBookingPlanInput) -> List[BookingPlanType]:
        try:
            values = await booking_plan_service.get_booking_plan_by_status(status)
            return [BookingPlanType.from_orm(value) for value in values]
        except Exception as e:
            raise strawberry.exceptions.StrawberryGraphQLError(f"Error getting booking plan by status: {e}")
    
