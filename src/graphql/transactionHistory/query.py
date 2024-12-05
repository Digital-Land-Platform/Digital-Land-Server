import strawberry
from uuid import UUID
from typing import List, Optional
from .services import TransactionHistoryService
from config.database import db
from src.models.TransactionHistory import TransactionHistory
from .types import TransactionHistoryType
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole


auth_management = AuthManagement()
transaction_service = TransactionHistoryService(db)

@strawberry.type
class TransactionHistoryQuery:
    
    @strawberry.field
    @auth_management.role_required([UserRole.ADMIN, UserRole.USER])
    async def get_transaction_history_by_property_id(self, property_id: UUID, info) -> Optional[TransactionHistoryType]:
        """
        Fetches transaction history by transaction_id, allowing access to admin, old owner, and current owner.
        
        Args:
            transaction_id (str): The ID of the transaction history to retrieve.
            user_id (str): The ID of the user requesting the data (to check if they are the owner or admin).
        
        Returns:
            TransactionHistory: The transaction history if authorized, None otherwise.
        """
        return await transaction_service.get_transaction_history_by_property_id(property_id)
