from sqlalchemy import Column, DateTime, String, Boolean, Date
from sqlalchemy.orm import relationship
from .OrganizationStaff import OrganizationStaff
from .Invitation import Invitation
from .OrganizationProfile import OrganizationProfile
from .OrganizationCertification import OrganizationCertification
from .OrganizationClient import OrganizationClient
from .Base import Base


class Organization(Base):
    __tablename__ = "organizations"
    
    name = Column(String, nullable=False)
    TIN = Column(String, nullable=False) # Tax Identifier Number
    issue_date = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=True)
    is_verified = Column(Boolean, default=False)
    verification_date = Column(DateTime, nullable=True)
    
    staff = relationship("OrganizationStaff", backref="organizations", cascade="all, delete-orphan")
    invitations = relationship("Invitation", backref="organizations", cascade="all, delete-orphan")
    organization = relationship("OrganizationProfile", backref="organizations", cascade="all, delete, delete-orphan")
    organization_certifications = relationship("OrganizationCertification", backref="organizations", cascade="all, delete-orphan")
    organizations_client = relationship("OrganizationClient", backref="organizations", cascade="all, delete-orphan")
