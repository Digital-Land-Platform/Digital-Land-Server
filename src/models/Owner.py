from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .Base import Base

class Owner(Base):
    __tablename__ = "owners"
    
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    address = Column(String, nullable=True)
    
    properties = relationship("Property", back_populates="owner")
