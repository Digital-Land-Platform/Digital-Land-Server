import strawberry
import enum


@strawberry.enum
class MessageEnum(enum.Enum):
    SENT = "Sent"
    DELIVERED = "Delivered"
    READ = "Read"

@strawberry.type
class MessageTypes:
    id: str
    sender_id: str
    receiver_id: str
    property_id: str | None = None
    transaction_id: str | None = None
    content: str
    status: str
    sent_at: str

    @classmethod
    def from_orm(cls, message):
        return cls(
            id=str(message.id),
            sender_id=message.sender_id,
            receiver_id=message.receiver_id,
            content=message.content,
            status=message.status.value,
            sent_at=message.sent_at.isoformat(),
            property_id=message.property_id,
            transaction_id=message.transaction_id
        )

@strawberry.input
class MessageInput:
    sender_id: str
    receiver_id: str
    content: str
    status: MessageEnum
    property_id: str | None = None
    transaction_id: str | None = None

@strawberry.input
class UpdateMessageInput:
    sender_id: str | None = None
    receiver_id: str | None = None
    content: str | None = None
    status: MessageEnum | None = None
    property_id: str | None = None
    transaction_id: str | None = None