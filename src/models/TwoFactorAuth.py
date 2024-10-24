from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .Base import Base
import uuid

class TwoFactorAuth(Base):
    __tablename__ = "two_factor_auth"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    otp_code = Column(String, nullable=False)