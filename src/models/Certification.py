from sqlalchemy import Column, String, Date, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .Base import Base
import uuid

class Certification(Base):
    __tablename__ = "certifications"
    
    certification_name = Column(String, nullable=False)
    issued_by = Column(String)
    certificate_url = Column(String)

    organizations_certification = relationship("OrganizationCertification", backref="certifications", cascade="all, delete-orphan")
