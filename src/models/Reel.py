from sqlalchemy import Column, ForeignKey, UUID, String, Text
from src.models.Base import Base 

class Reel(Base):
    __tablename__ = "reels"

    property_id = Column(UUID, ForeignKey("properties.id"))
    creator_id = Column(UUID, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String, nullable=False) 
    