import strawberry
from .services import InvitationService
from .types import InvitationType, InvitationInput
from src.middleware.AuthManagment import AuthManagement
from src.middleware.EmailHandler import EmailHandler
from config.database import db
from src.models.enums.UserRole import UserRole
from config.config import Config
from src.graphql.organization.service import OrganizationService

EMAIL_HOST = Config.get_env_variable("EMAIL_HOST")
EMAIL_PORT = Config.get_env_variable("EMAIL_PORT")
EMAIL_USERNAME = Config.get_env_variable("EMAIL_USERNAME")
EMAIL_PASSWORD = Config.get_env_variable("EMAIL_PASSWORD")
Audience = Config.get_env_variable("AUDUENCE")
auth_domian = Config.get_env_variable("AUTH_DOMAIN")
client_id = Config.get_env_variable("CLIENT_ID")
redirect_uri = Config.get_env_variable("REDIRECT_URI")

auth_management = AuthManagement()
invitation_service = InvitationService(db)
email_handler = EmailHandler(EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_HOST, EMAIL_PORT)
org_service = OrganizationService(db)

@strawberry.type
class InvitationMutation:

    @strawberry.mutation
    @auth_management.role_required([UserRole.ADMIN, UserRole.BROKER, UserRole.NOTARY, UserRole.USER])
    async def create_invitation(self, info, invitation_data: InvitationInput) -> InvitationType:
        try:
            token = info.context["request"].headers.get("Authorization").split(" ")[1]
            user_info = auth_management.get_user_info(token)
            invitation_data = vars(invitation_data)
            organization_name = await org_service.get_organization(invitation_data.get("organization_id"))
            invitation = await invitation_service.create_invitation(invitation_data, user_info.get("email"))
            invite_url = (
                    f"https://{auth_domian}/authorize"
                    "?response_type=code"
                    f"&client_id={client_id}"
                    f"&redirect_uri={redirect_uri}"
                    f"&scope=offline_access%20openid%20profile%20email%20read:users"
                    f"&audience={Audience}"
                    f"&state={invitation.id}"                    
                )
            
            email_handler.send_email(invitation.invitee_email,
                                      invite_url,invitation.invitee_name,
                                      organization_name.name)
            return InvitationType.from_orm(invitation)
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to create Invitation: {e}")

    @strawberry.mutation
    async def update_invitation(self, info, invitation_id: str, invitation_data: InvitationInput) -> InvitationType:
        try:
            invitation_data = vars(invitation_data)
            invitation = await invitation_service.update_invitation(invitation_id, invitation_data)
            return InvitationType.from_orm(invitation)
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to update Invitation: {e}")

    @strawberry.mutation
    async def delete_invitation(self, info, invitation_id: str) -> str:
        try:
            message = await invitation_service.delete_invitation(invitation_id)
            return message
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to delete Invitation: {e}")
        
    
    