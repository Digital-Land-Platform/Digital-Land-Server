from src.models.Invitation import Invitation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class InvitationRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_invitation(self, invitation: Invitation) -> Invitation:
        async with self.db:
            async with self.db.session as session:
                session.add(invitation)
                await session.commit()
                await session.refresh(invitation)
                return invitation

    async def update_invitation(self, invitationId: str, updatedInvitation: dict) -> Invitation:
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

    async def delete_invitation(self, invitationId: str) -> str:
        async with self.db:
            async with self.db.session as session:
                invitation = await session.get(Invitation, invitationId)
                if not invitation:
                    raise Exception("Invitation not found")
                await session.delete(invitation)
                await session.commit()
                return f"Invitation {invitationId} deleted"

    async def get_invitation_by_id(self, invitationId: str) -> Invitation:
        async with self.db:
            async with self.db.session as session:
                invitation = await session.get(Invitation, invitationId)
                if not invitation:
                    raise Exception("Invitation not found")
                return invitation

    async def get_all_invitations(self) -> list[Invitation]:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(select(Invitation))
                return result.scalars().all()
            