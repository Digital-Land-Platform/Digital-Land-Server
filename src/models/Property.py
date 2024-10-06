from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from src.models.Base import Base

class Property(Base):
    __tablename__ = "properties"
    
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    size = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    location = Column(String, nullable=False)
    neighborhood = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    images = Column(Text, nullable=False)
    virtualTourUrl = Column(String, nullable=True)
    streetViewUrl = Column(String, nullable=True)
    additionalFeatures = Column(Text, nullable=True)
    yearBuilt = Column(Integer, nullable=True)
    legalStatus = Column(String, nullable=False)
    disclosure = Column(Text, nullable=True)
    energyRating = Column(String, nullable=True)
    sustainabilityFeatures = Column(Text, nullable=True)
    futureDevelopmentPlans = Column(Text, nullable=True)
    zoningInformation = Column(Text, nullable=True)
    
    
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="properties")