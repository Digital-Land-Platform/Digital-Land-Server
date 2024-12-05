import strawberry
from uuid import UUID
from typing import List
from .services import TransactionHistoryService 
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole
from config.database import db

transaction_service = TransactionHistoryService(db)
auth_management = AuthManagement()

@strawberry.type
class TransactionHistoryMutation:
    
    @strawberry.mutation
    @auth_management.role_required([UserRole.ADMIN])
    async def delete_transaction_history(self, transaction_id: UUID, info) -> bool:
        """
        Delete a transaction history record.
        
        Args:
            transaction_id (UUID): The ID of the transaction history to delete.
        
        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            
            # Call the service method to delete the transaction history
            result = await transaction_service.delete_transaction_history(transaction_id)
            return result
        except Exception as e:
            raise Exception(f"Failed to delete transaction history: {e}")
