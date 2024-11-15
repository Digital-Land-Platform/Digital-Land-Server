from sqlalchemy import Column, String, Float, Date, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .enums.TransactionType import TransactionType
from .enums.TransactionStatus import TransactionStatus
from src.models.Payment import Payment
from src.models.Message import Message
from .Base import Base
import uuid

class Transaction(Base):
    __tablename__ = "transactions"
    
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=False)
    notary_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    transaction_number = Column(String, index=True, nullable=False, unique=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(TransactionStatus))
    transaction_date = Column(Date, nullable=True)
    payment_due_date = Column(Date, nullable=True)

    
    payment = relationship("Payment", uselist=False, backref="transactions", cascade="all, delete, delete-orphan")
    massage = relationship("Message", backref="transactions", cascade="all, delete, delete-orphan")
