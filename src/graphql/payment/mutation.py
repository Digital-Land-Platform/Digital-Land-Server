import strawberry
import strawberry.exceptions
from .service import PaymentService
from .types import PaymentTypes, PaymentInput, UpdatePaymentInput
from typing import List
from config.database import db
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole


auth_management = AuthManagement()
payment_service = PaymentService(db)

@strawberry.type
class PaymentMutation:

    @strawberry.mutation
    @auth_management.role_required([UserRole.NOTARY, UserRole.ADMIN, UserRole.USER, UserRole.BROKER])
    @auth_management.isAuth()
    async def create_payment(self, info, payment_data: PaymentInput) -> PaymentTypes:
        try:
            payment_data = vars(payment_data)
            payment_data["buyer_id"] = info.context.get("user_id")
            payment = await payment_service.create_payment(payment_data)
            return PaymentTypes.from_orm(payment)
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Error creating payment: {e}")
    
    @strawberry.mutation
    @auth_management.role_required([UserRole.NOTARY, UserRole.ADMIN, UserRole.USER, UserRole.BROKER])
    async def update_payment(self, info, payment_id: str, payment_data: UpdatePaymentInput) -> PaymentTypes:
        try:
            payment_data = vars(payment_data)
            payment = await payment_service.update_payment(payment_id, payment_data)
            return PaymentTypes.from_orm(payment)
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Error updating payment: {e}")
    
    @strawberry.mutation
    @auth_management.role_required([UserRole.NOTARY, UserRole.ADMIN, UserRole.USER, UserRole.BROKER])
    async def delete_payment(self, info, payment_id: str) -> PaymentTypes:
        try:
            payment = await payment_service.get_payment(payment_id)
            return PaymentTypes.from_orm(payment)
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Error deleting payment: {e}")


