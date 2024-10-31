from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
from datetime import datetime
import uuid
from src.models.Base import Base
#from .User import User
from src.models.UserRole import UserRole
from .Image import Image
from .Amenities import Amenities
from .Property_amenities import property_amenities


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
    virtualTourUrl = Column(String, nullable=True)
    streetViewUrl = Column(String, nullable=True)
    yearBuilt = Column(Integer, nullable=True)
    legalStatus = Column(String, nullable=False)
    disclosure = Column(Text, nullable=True)
    energyRating = Column(String, nullable=True)
    futureDevelopmentPlans = Column(Text, nullable=True)
    zoningInformation = Column(Text, nullable=True)
    
    
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="properties")
    
    images = relationship("Image", backref="properties", cascade="all, delete-orphan", lazy="joined")
    amenities = relationship('Amenities', secondary=property_amenities, backref='properties', lazy='joined')
    
    @validates('price')
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError("Price must be positive")
        return value

    @validates('size')
    def validate_size(self, key, value):
        if value <= 0:
            raise ValueError("Size must be positive")
        return value
    
    @validates('status')
    def check_status(self, key, value):
        valid_statuses = ['available', 'pending', 'sold']
        if value is not None and value not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}.')
        return value
    
    @validates('yearBuilt')
    def check_year_built(self, key, value):
        if value is not None and value < 0:
            raise ValueError('Year built must be a non-negative integer.')
        return value
    
    @validates('latitude')
    def check_latitude(self, key, value):
        if value is not None and not (-90 <= value <= 90):
            raise ValueError('Latitude must be between -90 and 90.')
        return value

    @validates('longitude')
    def check_longitude(self, key, value):
        if value is not None and not (-180 <= value <= 180):
            raise ValueError('Longitude must be between -180 and 180.')
        return value