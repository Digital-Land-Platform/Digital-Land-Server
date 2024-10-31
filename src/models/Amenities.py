from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
import uuid
from src.models.Base import Base 
from src.models.Property_amenities import property_amenities

class Amenities(Base):
    __tablename__ = 'amenities'

    #id = Column(UUID, primary_key=True, index=True)
    title = Column(String, nullable=False)
    icon = Column(String, nullable=False)

    # Relationship to Property
    #properties = relationship('Property', secondary=property_amenities, back_populates='amenities')