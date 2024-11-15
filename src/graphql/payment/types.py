import strawberry
import enum


@strawberry.enum
class PaymentMethod(enum.Enum):
    CREDIT_CARD = "Credit Card"
    BANK_TRANSFER = "Bank Transfer"
    CRYPTO = "Crypto"

@strawberry.type
class PaymentTypes:
    id: str
    transaction_id: str
    payment_method: str
    amount: float
    confirmed: bool
    transaction_fee: float
    payment_date: str

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
        )

@strawberry.input
class PaymentInput:
    transaction_id: str
    payment_method: PaymentMethod
    confirmed: bool
    transaction_fee: float
    payment_date: str | None = None

@strawberry.input
class UpdatePaymentInput:
    transaction_id: str | None = None
    payment_method: PaymentMethod | None = None
    confirmed: bool | None = None
    transaction_fee: float | None = None
    payment_date: str | None = None