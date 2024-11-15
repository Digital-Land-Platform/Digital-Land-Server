import strawberry
import strawberry.exceptions
from .services import AvailabilityService
from .types import AvailabilityType, AvailabilityInput, UpdateAvailabiltyInput
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole
from config.database import db


auth_manager = AuthManagement()
availabity_service = AvailabilityService(db)

@strawberry.type
class AvailabilityMutation:

    @strawberry.mutation
    @auth_manager.role_required([UserRole.ADMIN, UserRole.NOTARY])
    async def create_availability(self, info, availability_data: AvailabilityInput) -> AvailabilityType:
        try:
            availability_data = vars(availability_data)
            value = await availabity_service.create_availability(availability_data)
            return AvailabilityType.from_orm(value)
        except Exception as e:
            raise strawberry.exceptions.StrawberryGraphQLError(f"Error creating availability: {e}")

    @strawberry.mutation
    @auth_manager.role_required([UserRole.ADMIN, UserRole.NOTARY])
    async def update_availability(self, info, availability_id: str, availability_data: UpdateAvailabiltyInput) -> AvailabilityType:
        try:
            availability_data = vars(availability_data)
            value = await availabity_service.update_availability(availability_id, availability_data)
            return AvailabilityType.from_orm(value)
        except Exception as e:
            raise strawberry.exceptions.StrawberryGraphQLError(f"Error creating availability: {e}")

    @strawberry.mutation
    @auth_manager.role_required([UserRole.ADMIN, UserRole.NOTARY])
    async def delete_availability(self, info, availability_id: str) -> str:
        return await availabity_service.delete_availability(availability_id)
