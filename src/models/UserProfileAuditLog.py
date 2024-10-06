from sqlalchemy import Column, String, UUID, Enum
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.models.Base import Base
from src.models.AuditActions import AuditActions


class UserProfileAuditLog(Base):
    __tablename__ = "user_profile_audit_logs"
    user_profile_id = Column(UUID, index=True)
    entity = Column(String, nullable=False)  
    action = Column(Enum(AuditActions), nullable=False)  
    old_value = Column(String, nullable=True)
    new_value = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=False), server_default=func.now())