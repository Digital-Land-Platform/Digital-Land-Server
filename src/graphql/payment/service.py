from datetime import datetime
from src.models.repository.PaymentRepository import PaymentRepository
from src.models.Payment import Payment
from src.models.enums.PaymentMethod import PaymentMethod
from sqlalchemy.ext.asyncio import AsyncSession
from src.middleware.UserProfileValidator import UserProfileValidator
from src.graphql.transaction.services import TransactionService

class PaymentService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.payment_repo = PaymentRepository(self.db)
        self.transaction_service = TransactionService(self.db)
    
    async def create_payment(self, new_payment: dict) -> Payment:
        try:
            if "payment_method" in new_payment and new_payment.get("payment_method"):
                method_name = new_payment.get("payment_method").name
                new_payment["payment_method"] = getattr(PaymentMethod, method_name, None)
                if new_payment["payment_method"] is None:
                    raise ValueError(f"Invalid payment_method: {method_name}")
            transaction = await self.transaction_service.get_transaction(new_payment.get("transaction_id"))
            if not transaction:
                raise ValueError(f"Invalid transaction id: {new_payment.get('transaction_id')}")
            new_payment["amount"] = transaction.amount
            if new_payment.get("payment_date"):
                new_payment["payment_date"] = UserProfileValidator.change_str_date(new_payment.get("payment_date"))
            else:
                new_payment["payment_date"] = datetime.now()
            payment = await self.payment_repo.create_payment(Payment(**new_payment))
            return payment
        except Exception as e:
            raise Exception(f"Error creating payment: {e}")
    
    async def update_payment(self, payment_id: str, payment_data: dict) -> Payment:
        try:
            if "payment_method" in payment_data and payment_data.get("payment_method"):
                method_name = payment_data.get("payment_method").name
                payment_data["payment_method"] = getattr(PaymentMethod, method_name, None)
                if payment_data["payment_method"] is None:
                    raise ValueError(f"Invalid payment_method: {method_name}")
            if payment_data.get("payment_date"):
                payment_data["payment_date"] = UserProfileValidator.change_str_date(payment_data.get("payment_date"))
            else:
                payment_data["payment_date"] = datetime.now()
            payment = await self.payment_repo.update_payment(payment_id, payment_data)
            return payment
        except Exception as e:
            raise Exception(f"Error updating payment: {e}")
    
    async def get_payment(self, payment_id: str) -> Payment:
        try:
            return await self.payment_repo.get_payment(payment_id)
        except Exception as e:
            raise Exception(f"Error getting payment: {e}")
    
    async def delete_payment(self, payment_id: str) -> str:
        try:
            return await self.payment_repo.delete_payment(payment_id)
        except Exception as e:
            raise Exception(f"Error deleting payment: {e}")
    
    async def get_payments(self) -> list:
        try:
            return await self.payment_repo.get_all_payments()
        except Exception as e:
            raise Exception(f"Error getting payments: {e}")
    
    async def get_payments_by_confirm(self, confirm: bool) -> list:
        try:
            return await self.payment_repo.get_payments_confirmed(confirm)
        except Exception as e:
            raise Exception(f"Error getting payments by confirm: {e}")
    
    async def get_payment_by_payment_method(self, payment_method: PaymentMethod) -> list:
        try:
            if payment_method:
                payment_method = payment_method.name
                payment_method = getattr(PaymentMethod, payment_method, None)
                if not payment_method:
                    raise ValueError(f"Invalid payment_method: {payment_method}")
            return await self.payment_repo.get_payments_by_payment_method(payment_method)
        except Exception as e:
            raise Exception(f"Error getting payment by payment method: {e}")
    
    async def get_payment_by_transaction_id(self, transaction_id: str) -> Payment:
        try:
            return await self.payment_repo.get_payment_by_transaction_id(transaction_id)
        except Exception as e:
            raise Exception(f"Error getting payment by transaction id: {e}")
    
    


