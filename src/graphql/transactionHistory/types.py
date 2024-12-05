import strawberry
from uuid import UUID
from src.models.enums.TransactionType import TransactionType
from src.models.enums.TransactionStatus import TransactionStatus

@strawberry.type
class TransactionHistoryType:
    transaction_id: UUID
    buyer_id: UUID
    seller_id: UUID
    property_id: UUID
    notary_id: UUID
    transaction_type: TransactionType
    amount: float
    status: TransactionStatus
    transaction_date: str
