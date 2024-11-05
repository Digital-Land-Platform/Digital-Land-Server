from sqlalchemy import Column, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from .Base import Base
import uuid

class OrganizationCertification(Base):
    __tablename__ = "organization_certifications"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    certification_id = Column(UUID(as_uuid=True), ForeignKey("certifications.id"))
    issue_date = Column(Date)
    expiration_date = Column(Date)