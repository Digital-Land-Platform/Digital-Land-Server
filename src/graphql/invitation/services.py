from datetime import datetime
from src.models.Invitation import Invitation
from src.models.enums.InvitationStatus import InvitationStatus
from src.models.repository.InvitationRepository import InvitationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.enums.InvitationStatus import InvitationStatus
from src.graphql.userProfile.service import UserProfileService
from src.graphql.organization.service import OrganizationService
from src.middleware.AuthManagment import AuthManagement
from src.middleware.UserProfileValidator import UserProfileValidator
from src.models.enums.OrganizationRole import OrganizationRole



class InvitationService:
    def __init__(self, db: AsyncSession):
        self.invitation_repository = InvitationRepository(db)
        self.organization_service = OrganizationService(db)
        self.user_profile_service = UserProfileService(db)

    async def create_invitation(self, invitation: dict, user_email: str) -> dict:
        try:
            if "invitee_role" in invitation and invitation["invitee_role"]:
                invitation["invitee_role"] = getattr(OrganizationRole, invitation["invitee_role"].name)
            else:
                raise Exception("Invalid role change the invitee role")
            if "status" in invitation and invitation["status"]:
                invitation["status"] = getattr(InvitationStatus, invitation["status"].name)
            else:
                raise Exception("Invalid status change the status")
            if not await self.organization_service.get_organization(invitation.get("organization_id")):
                raise Exception("Organization not found")
            if not await self.user_profile_service.get_user_profile_by_id(invitation.get("inviter_id")):
                raise Exception("User not found")
            if invitation.get("sent_at"):
                invitation["sent_at"] = UserProfileValidator.change_str_date(invitation.get("sent_at"), "sent_at")
            else:
                invitation["sent_at"] = datetime.now()
            invitation_data = Invitation(**invitation)
            return await self.invitation_repository.create_invitation(invitation_data)
        except Exception as e:
            raise Exception(f"Failed to create invitation: {e}")

    async def update_invitation(self, invitation_id: str, updated_invitation: dict) -> dict:
        try:
            if "invitee_role" in updated_invitation and updated_invitation["invitee_role"]:
                updated_invitation["invitee_role"] = getattr(OrganizationRole, updated_invitation["invitee_role"].name)
            if "status" in updated_invitation and updated_invitation["status"]:
                updated_invitation["status"] = getattr(InvitationStatus, updated_invitation["status"].name)
            if updated_invitation.get("organization_id") and not await self.organization_service.get_organization(updated_invitation.get("organization_id")):
                raise Exception("Organization not found")
            if updated_invitation.get("inviter_id") and not await self.user_profile_service.get_user_profile_by_id(updated_invitation.get("inviter_id")):
                raise Exception("User not found")
            if updated_invitation.get("sent_at"):
                updated_invitation["sent_at"] = UserProfileValidator.change_str_date(updated_invitation.get("sent_at"), "sent_at")
            return await self.invitation_repository.update_invitation(invitation_id, updated_invitation)
        except Exception as e:
            raise Exception(f"Failed to update invitation: {e}")

    async def delete_invitation(self, invitation_id: str) -> str:
        try:
            return await self.invitation_repository.delete_invitation(invitation_id)
        except Exception as e:
            raise Exception(f"Failed to delete invitation: {e}")

    async def get_invitation_by_id(self, invitation_id: str) -> dict:
        try:
            return await self.invitation_repository.get_invitation_by_id(invitation_id)
        except Exception as e:
            raise Exception(f"Failed to get invitation: {e}")
    
    async def verify_invitation(self, invitation_id: str, user_email:str) -> bool:
        try:
            invitation = await self.invitation_repository.get_invitation_by_id(invitation_id)
            if invitation:
                updated_invitation = {
                    "status": InvitationStatus.ACCEPTED,
                    "responded_at":  datetime.now()
                }
                await self.update_invitation(invitation_id, updated_invitation)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"Failed to verify invitation: {e}")