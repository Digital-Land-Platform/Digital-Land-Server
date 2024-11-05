from sqlalchemy import Column, String, Text, Integer, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .Base import Base
import uuid

class OrganizationProfile(Base):
    __tablename__ = "organization_profiles"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    mission_statement = Column(Text)
    vision = Column(Text)
    values = Column(Text)
    description = Column(String)
    industry = Column(String)
    year_founded = Column(Integer)
    headquarters = Column(String)
    num_employees = Column(Integer)
    annual_revenue = Column(DECIMAL(15, 2))
    website_url = Column(String)
    logo_url = Column(String)
