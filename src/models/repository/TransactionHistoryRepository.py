from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.TransactionHistory import TransactionHistory
from typing import Optional
from uuid import UUID

from src.models.enums import TransactionType, TransactionStatus

class TransactionHistoryRepository:
    def __init__(self, db: AsyncSession):
        """
        Initializes the TransactionHistoryRepository with the database session.
        """
        self.db = db
        
    async def create_transaction_history(
        self,
        transaction_history: TransactionHistory
    ):
        async with self.db as session: 
            async with session.begin():  
                session.add(transaction_history)
            await session.commit()


    async def delete_transaction_history(self, transaction_id: str) -> bool:
        """
        Deletes a transaction history record by transaction ID.
        
        Args:
            transaction_id (str): The ID of the transaction history to be deleted.
        
        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        # Fetch the transaction history to be deleted
        async with self.db as session:
            transaction_history = await session.execute(select(TransactionHistory).where(TransactionHistory.id == transaction_id))
            transaction_history = transaction_history.scalar_one_or_none()

            if transaction_history:
                await session.delete(transaction_history)
                await session.commit()
                return True
            return False
    async def get_transaction_history_by_property_id(self, property_id: UUID) -> Optional[TransactionHistory]:
        """
        Retrieves a transaction history record by property ID.
        
        Args:
            transaction_id (str): The ID of the property history.
        
        Returns:
            Optional[TransactionHistory]: The transaction history if found, None otherwise.
        """
        async with self.db as session:
            result = await session.execute(
                select(TransactionHistory)
                .where(TransactionHistory.property_id == property_id)
            )
            return result.scalars().first()
    
    async def get_transaction_history_by_id(self, transaction_id: str) -> Optional[TransactionHistory]:
        
        async with self.db as session:
            result = await session.execute(
                select(TransactionHistory)
                .where(TransactionHistory.id == transaction_id)
            )
            return result.scalar_one_or_none()