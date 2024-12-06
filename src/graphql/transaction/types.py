import strawberry
import enum


@strawberry.enum
class TransactionEnum(enum.Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    DECLIEND = "Declined"

@strawberry.enum
class TransactionTypeEnum(enum.Enum):
    PURCHASE = "Purchase"
    TRANSFER = "Transfer"

@strawberry.type
class TransactionTypes:
    id: str
    buyer_id: str
    seller_id: str
    property_id: str
    notary_id: str
    transaction_number: str
    transaction_type: str
    amount: float
    status: str
    transaction_date: str
    payment_due_date: str

    @classmethod
    def from_orm(cls, transaction):
        return cls(
            id=str(transaction.id),
            buyer_id=transaction.buyer_id,
            seller_id=transaction.seller_id,
            property_id=transaction.property_id,
            notary_id=transaction.notary_id,
            transaction_number=transaction.transaction_number,
            transaction_type=transaction.transaction_type.value,
            amount=transaction.amount,
            status=transaction.status.value,
            transaction_date=transaction.transaction_date.isoformat(),
            payment_due_date=transaction.payment_due_date.isoformat(),
        )


@strawberry.input
class TransactionInput:
    property_id: str
    transaction_type: TransactionTypeEnum
    

@strawberry.input
class UpdateTransactionInput:
    buyer_id: str | None = None
    property_id: str | None = None
    transaction_type: TransactionTypeEnum | None = None
    status: TransactionEnum | None = None
    