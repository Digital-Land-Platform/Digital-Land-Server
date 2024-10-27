from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from uuid import UUID
from .Base import Base


# Join table for properties and amenities
property_amenities = Table(
    'property_amenity',
    Base.metadata,
    Column('property_id', ForeignKey('properties.id'), primary_key=True),
    Column('amenity_id', ForeignKey('amenities.id'), primary_key=True)
)