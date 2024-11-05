from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .UserProfile import UserProfile
from .Property import Property
from src.models.Base import Base
import uuid


class Location(Base):
    __tablename__ = "locations"
    province = Column(String, nullable=False)
    district = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    cell = Column(String, nullable=False)
    village = Column(String, nullable=False)
    city = Column(String)
    country = Column(String) 

    properties = relationship("Property", backref="locations", cascade="all, delete, delete-orphan")
    user_profiles = relationship("UserProfile", backref="locations", cascade="all, delete, delete-orphan")
