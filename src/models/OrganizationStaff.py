from sqlalchemy import Column, Date, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .Base import Base
from .enums.OrganizationRole import OrganizationRole

class OrganizationStaff(Base):
    __tablename__ = "organization_staff"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id"), nullable=False)
    role = Column(Enum(OrganizationRole),nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    
       
