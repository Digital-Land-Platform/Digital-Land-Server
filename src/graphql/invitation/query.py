import strawberry
from src.graphql.invitation.types import InvitationType
from src.graphql.invitation.services import InvitationService
from config.database import db

invitation_service = InvitationService(db)

@strawberry.type
class InvitationQuery:

    @strawberry.field
    async def get_invitation(self, invitation_id: str) -> InvitationType:
        try:
            invitation = await invitation_service.get_invitation(invitation_id)
            return InvitationType.from_orm(invitation)
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to get Invitation: {e}")
    
    async def get_invitations(self) -> list[InvitationType]:
        try:
            invitations = await invitation_service.get_all_invitations()
            return [InvitationType.from_orm(invitation) for invitation in invitations]
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to get Invitations: {e}")

