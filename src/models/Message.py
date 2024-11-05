from sqlalchemy import Column, String, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .enums.MessageStatus import MessageStatus
from .Base import Base
import uuid

class Message(Base):
    __tablename__ = "messages"
    
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=True)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("transactions.id"), nullable=True)
    content = Column(String, nullable=False)
    status = Column(Enum(MessageStatus), default=MessageStatus.SENT)
    sent_at = Column(TIMESTAMP, default="now()")
