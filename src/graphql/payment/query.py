from typing import List
import strawberry
from .types import PaymentMethod, PaymentTypes
from .service import PaymentService
from config.database import db
from src.models.enums.UserRole import UserRole
from src.middleware.AuthManagment import AuthManagement


auth_management = AuthManagement()
payment_service = PaymentService(db)

@strawberry.type
class PaymentQuery:
    
    @strawberry.field
    @auth_management.role_required([UserRole.NOTARY, UserRole.ADMIN, UserRole.USER, UserRole.BROKER])
    async def get_payments(self, info) -> List[PaymentTypes]:
        payments = await payment_service.get_payments()
        return [PaymentTypes.from_orm(payment) for payment in payments]

    @strawberry.field
    @auth_management.role_required([UserRole.NOTARY, UserRole.ADMIN, UserRole.USER, UserRole.BROKER])
    async def get_payment_by_id(self, info, payment_id: str) -> PaymentTypes:
        payment = await payment_service.get_payment(payment_id)
        return PaymentTypes.from_orm(payment)

    @strawberry.field
    @auth_management.role_required([UserRole.NOTARY, UserRole.ADMIN, UserRole.USER, UserRole.BROKER])
    async def get_payments_by_transaction_id(self, info, transaction_id: str) -> PaymentTypes:
        payment = await payment_service.get_payment_by_transaction_id(transaction_id)
        return PaymentTypes.from_orm(payment)

    @strawberry.field
    @auth_management.role_required([UserRole.NOTARY, UserRole.ADMIN, UserRole.USER, UserRole.BROKER])
    async def get_payments_by_payment_method(self, info, payment_method: PaymentMethod) -> List[PaymentTypes]:
        payments = await payment_service.get_payment_by_payment_method(payment_method)
        return [PaymentTypes.from_orm(payment) for payment in payments]

    @strawberry.field
    @auth_management.role_required([UserRole.NOTARY, UserRole.ADMIN, UserRole.USER, UserRole.BROKER])
    async def get_payments_by_confirmed(self, info, confirmed: bool) -> List[PaymentTypes]:
        payments = await payment_service.get_payments_by_confirm(confirmed)
        return [PaymentTypes.from_orm(payment) for payment in payments]   