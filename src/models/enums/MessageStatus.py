import enum

class MessageStatus(enum.Enum):
    SENT = "Sent"
    DELIVERED = "Delivered"
    READ = "Read"