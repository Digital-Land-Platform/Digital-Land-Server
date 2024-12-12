from sqlalchemy import Column, Float, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .enums.PaymentMethod import PaymentMethod
from .Base import Base
import uuid

class Payment(Base):
    __tablename__ = "payments"
    
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("transactions.id"), unique=True)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    amount = Column(Float, nullable=False)
    confirmed = Column(Boolean, default=False)
    transaction_fee = Column(Float, default=0.0)
    notary_fee = Column(Float, default=0.0)
    payment_date = Column(DateTime(timezone=True), nullable=True)
