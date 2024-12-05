import enum
import strawberry

@strawberry.enum
class TransactionType(enum.Enum):
    PURCHASE = "Purchase"
    TRANSFER = "Transfer"