from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .enums.OrganizationRole import OrganizationRole
from .Base import Base
from .enums.InvitationStatus import InvitationStatus
import uuid

class Invitation(Base):
    __tablename__ = "invitations"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    inviter_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id"), nullable=False)
    invitee_email = Column(String, nullable=False)
    invitee_name = Column(String, nullable=False)
    invitee_role = Column(Enum(OrganizationRole), nullable=False)
    status = Column(Enum(InvitationStatus), default=InvitationStatus.PENDING)
    sent_at = Column(DateTime(timezone=True))
    responded_at = Column(DateTime(timezone=True))