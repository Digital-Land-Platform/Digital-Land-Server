import strawberry
from uuid import UUID
from typing import List
from src.services import TransactionHistoryService  # assuming services are correctly set up
from src.models import UserRole, TransactionHistory
from src.utils import auth_management  # Assuming you have an auth utility for role management

transaction_service = TransactionHistoryService()

@strawberry.type
class TransactionHistoryMutation:
    
    @strawberry.mutation
    @auth_management.role_required([UserRole.ADMIN])  # Only Admins can delete a transaction history
    async def delete_transaction_history(self, transaction_id: UUID, info) -> bool:
        """
        Delete a transaction history record.
        
        Args:
            transaction_id (UUID): The ID of the transaction history to delete.
        
        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            # Get the token from the request context
            token = info.context["request"].headers.get("authorization").split(" ")[1]
            user_info = auth_management.get_user_info(token)

            # Fetch the user from the database based on the info retrieved from the token
            user = await user_service.get_user_by_email(user_info.get("email"))
            
            # Call the service method to delete the transaction history
            result = await transaction_service.delete_transaction_history(transaction_id, user.id)
            return result
        except Exception as e:
            raise Exception(f"Failed to delete transaction history: {e}")
