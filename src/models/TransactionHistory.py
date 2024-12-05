from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .Base import Base
from src.models.Transaction import Transaction
from src.models.User import User
from src.models.Property import Property
from src.models.enums. TransactionType import TransactionType
from src.models.enums.TransactionStatus import TransactionStatus

class TransactionHistory(Base):
    __tablename__ = "transaction_history"
    

    transaction_id = Column(UUID(as_uuid=True), ForeignKey("transactions.id"), nullable=False)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=False)
    notary_id = Column(UUID, nullable=True)
    amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    transaction_type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), nullable=False)
    
    # Relationships
    transaction = relationship("Transaction", backref="history", uselist=False)
    buyer = relationship("User", foreign_keys=[buyer_id], backref="buy_transactions")
    seller = relationship("User", foreign_keys=[seller_id], backref="sell_transactions")
    property = relationship("Property", backref="transactions_history")
    
    