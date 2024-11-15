import strawberry
from uuid import UUID

@strawberry.type
class TransactionHistory:
    transaction_id: UUID
    buyer_id: UUID
    seller_id: UUID
    property_id: UUID
    notary_id: UUID
    transaction_type: str
    amount: float
    status: str
    transaction_date: str 
