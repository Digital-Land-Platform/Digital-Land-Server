from datetime import datetime
from src.models.Payment import Payment
from sqlalchemy import select
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession

class PaymentRepository:

    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_payment(self, new_payment: Payment) -> Payment:
        try:
            async with self.db:
                async with self.db.session as session:
                    session.add(new_payment)
                    await session.commit()
                    await session.refresh(new_payment)
                    return new_payment
        except Exception as e:
            raise Exception(f"Error creating payment: {e}")
        
    async def update_payment(self, payment_id: str, payment_data: Dict) -> Payment:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Payment).where(Payment.id == payment_id)
                    )
                    payment = result.scalar_one_or_none()
                    for key, value in payment_data.items():
                        if value and hasattr(payment, key):
                            setattr(payment, key, value)
                    payment.updated_at = datetime.now()
                    session.add(payment)
                    await session.commit()
                    await session.refresh(payment)
                    return payment
        except Exception as e:
            raise Exception(f"Error updating payment: {e}")
    
    async def get_payment(self, payment_id: str) -> Payment:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Payment).where(Payment.id == payment_id)
                    )
                    return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error getting payment: {e}")
    
    async def delete_payment(self, payment_id: str) -> str:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Payment).where(Payment.id == payment_id)
                    )
                    payment = result.scalar_one_or_none()
                    await session.delete(payment)
                    await session.commit()
                    return payment
        except Exception as e:
            raise Exception(f"Error deleting payment: {e}")
    
    async def get_all_payments(self) -> List[Payment]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Payment)
                    )
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error getting all payments: {e}")
    
    async def get_payments_confirmed(self, confirm: bool) -> List[Payment]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Payment).where(Payment.confirmed == confirm)
                    )
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error getting confirmed payments: {e}")
    
    async def get_payments_by_payment_method(self, payment_method: str) -> List[Payment]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Payment).where(Payment.payment_method == payment_method)
                    )
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error getting payments by payment method: {e}")
    
    async def get_payment_by_transaction_id(self, transaction_id: str) -> Payment:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Payment).where(Payment.transaction_id == transaction_id)
                    )
                    return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error getting payment by transaction ID: {e}")