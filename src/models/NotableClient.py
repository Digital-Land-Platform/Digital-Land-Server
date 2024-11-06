from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .Base import Base
import uuid

class NotableClient(Base):
    __tablename__ = "clients"
    
    client_name = Column(String, nullable=False)
    industry = Column(String)
    logo_url = Column(String)

    organizations_client = relationship("OrganizationClient", backref="clients", cascade="all, delete-orphan")
