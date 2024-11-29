from sqlalchemy import Column, Text, String
from sqlalchemy.orm import relationship
from .Base import Base
from .PropertyCatagoryRelation import PropertyCatagoryRelation

class PropertyCatagories(Base):

    __tablename__ = 'property_catagories'

    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    properties = relationship("PropertyCatagoryRelation", backref="property_catagories")