from sqlalchemy import Column, String, Date
from sqlalchemy import ForeignKey,UUID
from sqlalchemy.orm import relationship
from src.models.OrganizationStaff import OrganizationStaff
from src.models.Invitation import Invitation
from .Base import Base

class UserProfile(Base):

    __tablename__ = "user_profiles"
    user_id = Column(UUID, ForeignKey("users.id"), unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    location_id = Column(UUID, ForeignKey("locations.id"))
    date_of_birth = Column(Date)
    license_number = Column(String)

    organization_staff = relationship("OrganizationStaff", backref="user_profiles", cascade="all, delete, delete-orphan")
    invitater = relationship("Invitation", backref="user_profiles", cascade="all, delete, delete-orphan")