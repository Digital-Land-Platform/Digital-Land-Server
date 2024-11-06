from src.models.Invitation import Invitation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class InvitationRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_invitation(self, invitation: Invitation) -> Invitation:
        try:
            async with self.db:
                async with self.db.session as session:
                    session.add(invitation)
                    await session.commit()
                    await session.refresh(invitation)
                    return invitation
        except Exception as e:
            raise Exception(f"Failed to create invitation: {e}")
    
    async def update_invitation(self, invitationId: str, updatedInvitation: dict) -> Invitation:
        try:
            async with self.db:
                async with self.db.session as session:
                    invitation = await session.get(Invitation, invitationId)
                    if not invitation:
                        raise Exception("Invitation not found")
                    for key, value in updatedInvitation.items():
                        if value and hasattr(invitation, key):
                            setattr(invitation, key, value)
                    session.add(invitation)
                    await session.commit()
                    await session.refresh(invitation)
                    return invitation
        except Exception as e:
            raise Exception(f"Failed to update invitation: {e}")
    
    async def delete_invitation(self, invitationId: str) -> str:
        try:
            async with self.db:
                async with self.db.session as session:
                    invitation = await session.get(Invitation, invitationId)
                    if not invitation:
                        raise Exception("Invitation not found")
                    await session.delete(invitation)
                    await session.commit()
                    return f"Invitation {invitationId} deleted"
        except Exception as e:
            raise Exception(f"Failed to delete invitation: {e}")
    
    async def get_invitation_by_id(self, invitationId: str) -> Invitation:
        try:
            async with self.db:
                async with self.db.session as session:
                    invitation = await session.get(Invitation, invitationId)
                    if not invitation:
                        raise Exception("Invitation not found")
                    return invitation
        except Exception as e:
            raise Exception(f"Failed to get invitation: {e}")
    
    async def get_all_invitations(self) -> list[Invitation]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(select(Invitation))
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Failed to get all invitations: {e}")