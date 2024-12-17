from datetime import datetime
from src.models.Payment import Payment
from sqlalchemy import select
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession

class PaymentRepository:

    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_payment(self, new_payment: Payment) -> Payment:
        async with self.db:
            async with self.db.session as session:
                session.add(new_payment)
                await session.commit()
                await session.refresh(new_payment)
                return new_payment
    
    async def update_payment(self, payment_id: str, payment_data: Dict) -> Payment:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Payment).where(Payment.id == payment_id)
                )
                payment = result.scalar_one_or_none()
                for key, value in payment_data.items():
                    if value and hasattr(payment, key):
                        setattr(payment, key, value)
                session.add(payment)
                await session.commit()
                await session.refresh(payment)
                return payment

    async def get_payment(self, payment_id: str) -> Payment:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Payment).where(Payment.id == payment_id)
                )
                return result.scalar_one_or_none()

    async def delete_payment(self, payment_id: str) -> str:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Payment).where(Payment.id == payment_id)
                )
                payment = result.scalar_one_or_none()
                await session.delete(payment)
                await session.commit()
                return payment

    async def get_all_payments(self) -> List[Payment]:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Payment)
                )
                return result.scalars().all()

    async def get_payments_confirmed(self, confirm: bool) -> List[Payment]:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Payment).where(Payment.confirmed == confirm)
                )
                return result.scalars().all()

    async def get_payments_by_payment_method(self, payment_method: str) -> List[Payment]:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Payment).where(Payment.payment_method == payment_method)
                )
                return result.scalars().all()

    async def get_payment_by_transaction_id(self, transaction_id: str) -> Payment:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Payment).where(Payment.transaction_id == transaction_id)
                )
                return result.scalar_one_or_none()
