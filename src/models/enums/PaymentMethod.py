import enum

class PaymentMethod(enum.Enum):
    CREDIT_CARD = "Credit Card"
    BANK_TRANSFER = "Bank Transfer"
    CRYPTO = "Crypto"
    MOBILE_MONEY = "Mobile Money"
    PAYPAL = "Paypal"
