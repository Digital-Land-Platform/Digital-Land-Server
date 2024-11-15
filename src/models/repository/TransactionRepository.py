from datetime import datetime
from typing import Dict, List
from sqlalchemy import select
from src.models.Transaction import Transaction


class TransactionRepository:

    def __init__(self, db):
        self.db = db
    
    async def create_transaction(self, new_transaction: Transaction) -> Transaction:
        try:
            async with self.db:
                async with self.db.session as session:
                    session.add(new_transaction)
                    await session.commit()
                    await session.refresh(new_transaction)
                    return new_transaction
        except Exception as e:
            raise Exception(f"Error creating transaction: {e}")
        
    async def update_transaction(self, transaction_id: str, transaction_data: Dict) -> Transaction:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Transaction).where(Transaction.id == transaction_id)
                    )
                    transaction = result.scalar_one_or_none()
                    if not transaction:
                        raise Exception("Fail to update transaction not found")
                    for key, value in transaction_data.items():
                        if value and hasattr(transaction, key):
                            setattr(transaction, key, value)
                    setattr(transaction, "updated_at", datetime.now())
                    session.add(transaction)
                    await session.commit()
                    await session.refresh(transaction)
                    return transaction
        except Exception as e:
            raise Exception(f"Error updating transaction: {e}")
    
    async def get_transaction(self, transaction_id: str) -> Transaction:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Transaction).where(Transaction.id == transaction_id)
                    )
                    return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error getting transaction: {e}")
    
    async def delete_transaction(self, transaction_id: str) -> str:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Transaction).where(Transaction.id == transaction_id)
                    )
                    transaction = result.scalars().first()
                    await session.delete(transaction)
                    await session.commit()
                    return f"Transaction {transaction_id} deleted"
        except Exception as e:
            raise Exception(f"Error deleting transaction: {e}")
    
    async def get_transactions(self) -> List[Transaction]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(select(Transaction))
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error getting transactions: {e}")
    
    async def get_transactions_by_buyer_id(self, user_id: str) -> List[Transaction]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Transaction).where(Transaction.buyer_id == user_id)
                    )
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error getting transactions: {e}")
    
    async def get_transactions_by_seller_id(self, user_id: str) -> List[Transaction]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Transaction).where(Transaction.seller_id == user_id)
                    )
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error getting transactions: {e}")
        
    async def get_transactions_by_property_id(self, property_id: str) -> List[Transaction]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Transaction).where(Transaction.property_id == property_id)
                    )
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error getting transactions: {e}")
    
    async def get_transactions_by_notary_id(self, notary_id: str) -> List[Transaction]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Transaction).where(Transaction.notary_id == notary_id)
                    )
                return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error getting transactions: {e}")
    
    async def get_transactions_by_status(self, status: str) -> List[Transaction]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Transaction).where(Transaction.status == status)
                    )
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error getting transactions: {e}")
    
    async def get_transactions_by_type(self, transaction_type: str) -> List[Transaction]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Transaction).where(Transaction.transaction_type == transaction_type)
                    )
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error getting transactions: {e}")
    
    async def get_transaction_by_transaction_number(self, transaction_number: str) -> Transaction:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Transaction).where(Transaction.transaction_number == transaction_number)
                    )
                    return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error getting transaction: {e}")
    
    
