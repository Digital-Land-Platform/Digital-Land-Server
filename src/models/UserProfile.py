from sqlalchemy import Column, String, Integer
from sqlalchemy import ForeignKey,UUID
from .Base import Base
from src.models.UserProfileAuditLog import UserProfileAuditLog

class UserProfile(Base):

    __tablename__ = "user_profiles"
    user_id = Column(UUID, ForeignKey("users.id"), unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    physical_address = Column(String)
    identity_card_number = Column(String)
    whatsapp_number = Column(String)
    smart_contract = Column(String)
