from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .enums.NotificationType import NotificationType
from .enums.MessageStatus import MessageStatus
from .Base import Base
import uuid

class Notification(Base):
    __tablename__ = "notifications"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)
    message_type = Column(Enum(NotificationType), default=NotificationType.REMINDER)
    status = Column(Enum(MessageStatus), default=MessageStatus.SENT)
    sent_at = Column(DateTime(timezone=True), default="now()")
