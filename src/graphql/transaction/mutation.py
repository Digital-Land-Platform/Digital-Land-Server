import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .services import TransactionService
from .types import TransactionTypes, TransactionInput, UpdateTransactionInput, TransactionEnum
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole
from config.database import db

transaction_service = TransactionService(db)
auth_management = AuthManagement()

@strawberry.type
class TransactionMutation:

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def create_transaction(self, info, transaction_data: TransactionInput) -> TransactionTypes:
        transaction_data = vars(transaction_data)
        transaction = await transaction_service.create_transaction(transaction_data)
        return TransactionTypes.from_orm(transaction)

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def update_transaction(self, info, transaction_id: str, transaction_data: UpdateTransactionInput) -> TransactionTypes:
        transaction_data = vars(transaction_data)
        transaction = await transaction_service.update_transaction(transaction_id, transaction_data)
        return TransactionTypes.from_orm(transaction)

    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def delete_transaction(self, info, transaction_id: str) -> str:
        return await transaction_service.delete_transaction(transaction_id)
    
    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.NOTARY, UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def confirm_transaction(self, info, transaction_id: str, status: TransactionEnum) -> TransactionTypes:
        transaction = await transaction_service.notary_approval(transaction_id, status)
        return TransactionTypes.from_orm(transaction)