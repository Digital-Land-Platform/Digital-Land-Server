from src.graphql.transaction.types import TransactionInput
import strawberry
import enum


@strawberry.enum
class PaymentMethod(enum.Enum):
    CREDIT_CARD = "Credit Card"
    BANK_TRANSFER = "Bank Transfer"
    CRYPTO = "Crypto"
    MOBILE_MONEY = "Mobile Money"
    PAYPAL = "Paypal"

@strawberry.type
class PaymentTypes:
    id: str
    transaction_id: str
    payment_method: str
    amount: float
    confirmed: bool
    transaction_fee: float
    payment_date: str
    notary_fee: float

    @classmethod
    def from_orm(cls, payment):
        return cls(
            id=str(payment.id),
            transaction_id=payment.transaction_id,
            payment_method=payment.payment_method.value,
            amount=payment.amount,
            confirmed=payment.confirmed,
            transaction_fee=payment.transaction_fee,
            payment_date=payment.payment_date.isoformat(),
            notary_fee=payment.notary_fee
        )

@strawberry.input
class PaymentInput(TransactionInput):
    payment_method: PaymentMethod
    
@strawberry.input
class UpdatePaymentInput:
    transaction_id: str | None = None
    payment_method: PaymentMethod | None = None
    confirmed: bool | None = None
    transaction_fee: float | None = None
    payment_date: str | None = None
