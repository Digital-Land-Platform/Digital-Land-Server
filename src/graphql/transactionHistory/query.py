import strawberry
from typing import List, Optional
from .services import TransactionHistoryService

transaction_service = TransactionHistoryService(db.SessionLocal())

@strawberry.type
class TransactionHistoryQuery:
    @strawberry.field
    async def get_transaction_history_by_property_id(self, property_id: str, user_id: str) -> Optional[TransactionHistory]:
        """
        Fetches transaction history by transaction_id, allowing access to admin, old owner, and current owner.
        
        Args:
            transaction_id (str): The ID of the transaction history to retrieve.
            user_id (str): The ID of the user requesting the data (to check if they are the owner or admin).
        
        Returns:
            TransactionHistory: The transaction history if authorized, None otherwise.
        """
        return await transaction_service.get_transaction_history_by_property_id(property_id, user_id)
