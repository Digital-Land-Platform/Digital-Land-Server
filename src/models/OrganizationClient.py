from sqlalchemy import Column, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .Base import Base
import uuid

class OrganizationClient(Base):
    __tablename__ = "organization_clients"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"))
    engagement_start_date = Column(Date)
    engagement_end_date = Column(Date)
