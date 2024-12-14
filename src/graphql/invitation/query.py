import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from src.graphql.invitation.types import InvitationType
from src.graphql.invitation.services import InvitationService
from config.database import db
from src.middleware.AuthManagment import AuthManagement

auth_management = AuthManagement()
invitation_service = InvitationService(db)

@strawberry.type
class InvitationQuery:

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_invitation(self, invitation_id: str) -> InvitationType:
        invitation = await invitation_service.get_invitation(invitation_id)
        return InvitationType.from_orm(invitation)

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_invitations(self) -> list[InvitationType]:
        invitations = await invitation_service.get_all_invitations()
        return [InvitationType.from_orm(invitation) for invitation in invitations]


