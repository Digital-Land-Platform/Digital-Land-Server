import strawberry
import enum
from src.graphql.organizatoinStaff.types import OrganizationStaffRole

@strawberry.enum
class InvitationStatus(enum.Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    Decliend = "Declined"

@strawberry.type
class InvitationType:
    organization_id: str | None
    inviter_id: str | None
    invitee_email: str | None
    invitee_name: str | None
    invitee_role: str | None
    status: str | None
    sent_at: str | None
    responded_at: str | None

    @classmethod
    def from_orm(cls, invitation):
        return cls(
            organization_id=invitation.organization_id,
            inviter_id=invitation.inviter_id,
            invitee_email=invitation.invitee_email,
            invitee_name=invitation.invitee_name,
            invitee_role=invitation.invitee_role.value,
            status=invitation.status.value,
            sent_at=invitation.sent_at.isoformat(),
            responded_at=invitation.responded_at.isoformat() if invitation.responded_at else None
        )

@strawberry.input
class InvitationInput:
    organization_id: str | None = None
    inviter_id: str | None = None
    invitee_email: str | None = None
    invitee_name: str | None = None
    invitee_role: OrganizationStaffRole | None = None
    status: InvitationStatus | None = None
    sent_at: str | None = None