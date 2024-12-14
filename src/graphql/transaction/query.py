import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .types import TransactionTypes
from typing import List
from .services import TransactionService
from config.database import db
from .types import TransactionEnum, TransactionTypeEnum
from src.middleware.AuthManagment import AuthManagement

auth_management = AuthManagement()
transaction_service = TransactionService(db)

@strawberry.type
class TransactionQuery:

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_transactions(self, info) -> List[TransactionTypes]:
        transactions = await transaction_service.get_transactions()
        return [TransactionTypes.from_orm(transaction) for transaction in transactions]

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_transaction_by_id(self, info, transaction_id: str) -> TransactionTypes:
        transaction = await transaction_service.get_transaction(transaction_id)
        return TransactionTypes.from_orm(transaction)

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_transactions_by_seller_id(self, info, user_id: str) -> List[TransactionTypes]:
        transactions = await transaction_service.get_transaction_by_seller_id(user_id)
        return [TransactionTypes.from_orm(transaction) for transaction in transactions]

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_transactions_by_property_id(self, info, property_id: str) -> List[TransactionTypes]:
        transactions = await transaction_service.get_transactions_by_property(property_id)
        return [TransactionTypes.from_orm(transaction) for transaction in transactions]

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_transactions_by_notary_id(self, info, notary_id: str) -> List[TransactionTypes]:
        transactions = await transaction_service.get_transaction_by_notary_id(notary_id)
        return [TransactionTypes.from_orm(transaction) for transaction in transactions]

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_transactions_by_status(self, info, status: TransactionEnum) -> List[TransactionTypes]:
        transactions = await transaction_service.get_transactions_by_status(status)
        return [TransactionTypes.from_orm(transaction) for transaction in transactions]

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_transactions_by_type(self, info, transaction_type: TransactionTypeEnum) -> List[TransactionTypes]:
        transactions = await transaction_service.get_transactions_by_type(transaction_type)
        return [TransactionTypes.from_orm(transaction) for transaction in transactions]
    
    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_transaction_by_transaction_number(self, info, transaction_number: str) -> TransactionTypes:
        transaction = await transaction_service.get_transaction_by_transaction_number(transaction_number)
        return TransactionTypes.from_orm(transaction)
    
    