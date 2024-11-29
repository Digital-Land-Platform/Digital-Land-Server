from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base


class PropertyCatagoryRelation(Base):
    __tablename__ = "property_catagory_relations"

    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), primary_key=True)
    catagory_id = Column(UUID(as_uuid=True), ForeignKey("property_catagories.id"), primary_key=True)
