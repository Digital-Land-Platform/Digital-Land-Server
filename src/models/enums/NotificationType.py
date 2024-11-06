import enum

class NotificationType(enum.Enum):
    TRANSACTION = "Transaction"
    REMINDER = "Reminder"
    SYSTEM = "System"