from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from src.models.Base import Base

class PropertyHistory(Base):
    __tablename__ = "property_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    size = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="sold")  # Always sold for history
    location = Column(String, nullable=False)
    neighborhood = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    images = Column(String, nullable=False)
    owner_id = Column(UUID(as_uuid=True), nullable=False)  # Previous owner (seller)
    sale_date = Column(DateTime, default=datetime.utcnow)  # When the sale was finalized
