from sqlalchemy import Column, String, UUID, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .Base import Base
import uuid

class Amenity(Base):
    __tablename__ = "amenities"
    
    title = Column(String, nullable=False)
    icon = Column(String) 
    
