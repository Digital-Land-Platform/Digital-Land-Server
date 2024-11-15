from typing import Optional
from src.repositories.TransactionHistoryRepository import TransactionHistoryRepository
from src.models.User import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from src.models.TransactionHistory import TransactionHistory

class TransactionHistoryService:
    def __init__(self, db: AsyncSession):
        """
        Initializes the TransactionHistoryService with the database session.
        """
        self.db = db
        self.repository = TransactionHistoryRepository(db)

    async def delete_transaction_history(self, transaction_id: UUID, user_id: str) -> bool:
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
        
        # Perform permission check, e.g., verify the user is the admin or property owner
        if transaction_history.user_id != user_id:
            raise PermissionError("You are not authorized to delete this transaction history.")
        
        # Proceed with deletion
        return await self.repository.delete_transaction_history(transaction_id)
    
    
    async def get_transaction_history_by_property_id(self, property_id: UUID, user_id: UUID) -> Optional[TransactionHistory]:
        """
        Retrieves a transaction history by its ID, ensuring that the user is authorized.
        
        Args:
            transaction_id (str): The ID of the transaction history to retrieve.
            user_id (str): The ID of the user requesting the transaction history.
        
        Returns:
            TransactionHistory: The transaction history object if authorized, None otherwise.
        """
        # Fetch the transaction history by ID using the repository
        transaction_history = await self.repository.get_transaction_history_by_property_id(property_id)
        
        if not transaction_history:
            return None
        
        # Authorization check: only the current owner, admin, or specific user can access
        if transaction_history.user_id == user_id or user_id == "admin":
            return transaction_history
        
        # If the user does not have the proper authorization, return None or raise an exception
        return None