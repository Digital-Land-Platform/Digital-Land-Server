from typing import Optional
from src.models.repository.TransactionHistoryRepository import TransactionHistoryRepository
from src.models.repository.TransactionRepository import TransactionRepository
from src.models.enums.TransactionStatus import TransactionStatus
from src.models.enums.TransactionType import TransactionType
from src.graphql.transaction.services import TransactionService
from src.models.User import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from src.models.TransactionHistory import TransactionHistory
from uuid import UUID
from config.database import db
from .types import TransactionHistoryType
from src.models.enums.PropertyStatus import PropertyStatus
from src.graphql.property.services import PropertyService


class TransactionHistoryService:
    def __init__(self, db: AsyncSession):
        """
        Initializes the TransactionHistoryService with the database session.
        """
        self.db = db
        self.repository = TransactionHistoryRepository(db)
        self.transaction_repo = TransactionRepository(self.db)
        self.property_service = PropertyService(db)
        self.transaction_service = TransactionService(self.db)
          
    async def create_transaction_history(
        self,
        transaction_id: UUID,
        buyer_id: UUID,
        seller_id: UUID,
        property_id: UUID,
        amount: float,
        transaction_type: TransactionType,
        status: TransactionStatus,
    ):
        """Create a TransactionHistory record and delegate database interaction."""
        new_history = TransactionHistory(
            transaction_id=transaction_id,
            buyer_id=buyer_id,
            seller_id=seller_id,
            property_id=property_id,
            amount=amount,
            transaction_type=transaction_type,
            status=status,
        )
        # Delegate saving to the repository
        await self.repository.create_transaction_history(new_history)
    async def delete_transaction_history(self, transaction_id: UUID) -> bool:
        """
        Deletes a transaction history entry from the database.
        
        Args:
            transaction_id (UUID): The ID of the transaction history.
            user_id (str): The ID of the user requesting the deletion.
        
        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        # Check if the transaction history exists
        transaction_history = await self.repository.get_transaction_history_by_id(transaction_id)
        
        if not transaction_history:
            raise Exception("Transaction history not found.")
        
        return await self.repository.delete_transaction_history(transaction_id)
    
    
    async def get_transaction_history_by_property_id(self, property_id: UUID) -> Optional[TransactionHistoryType]:
        """
        Retrieves a transaction history by its ID, ensuring that the user is authorized.
        
        Args:
            transaction_id (str): The ID of the transaction history to retrieve.
            user_id (str): The ID of the user requesting the transaction history.
        
        Returns:
            TransactionHistory: The transaction history object if authorized, None otherwise.
        """
        try:
            # Fetch the transaction history by ID using the repository
            transaction_history = await self.repository.get_transaction_history_by_property_id(property_id)
        
            if not transaction_history:
                print(f"No transaction history found for property_id: {property_id}")
                return None
        
            return TransactionHistoryType(
                transaction_id=transaction_history.transaction_id,
                buyer_id=transaction_history.buyer_id,
                seller_id=transaction_history.seller_id,
                property_id=transaction_history.property_id,
                notary_id=transaction_history.notary_id,
                transaction_type=transaction_history.transaction_type,
                amount=transaction_history.amount,
                status=transaction_history.status,
                transaction_date=transaction_history.transaction_date
            )
        except Exception as e:
            print(f"An error occurred while fetching transaction history: {e}")
            return None