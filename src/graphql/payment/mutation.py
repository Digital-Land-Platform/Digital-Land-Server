import strawberry
import strawberry.exceptions
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
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
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def create_payment(self, info, payment_data: PaymentInput) -> PaymentTypes:
        payment_data = vars(payment_data)
        payment_data["buyer_id"] = info.context.get("user_id")
        payment = await payment_service.create_payment(payment_data)
        return PaymentTypes.from_orm(payment)
    
    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def update_payment(self, info, payment_id: str, payment_data: UpdatePaymentInput) -> PaymentTypes:
        payment_data = vars(payment_data)
        payment = await payment_service.update_payment(payment_id, payment_data)
        return PaymentTypes.from_orm(payment)
