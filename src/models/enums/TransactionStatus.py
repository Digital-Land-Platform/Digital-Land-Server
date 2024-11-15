import enum

class TransactionStatus(enum.Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    DECLIEND = "Declined"