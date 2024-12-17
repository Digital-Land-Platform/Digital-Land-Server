from src.models.NotableClient import NotableClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class NotableClientRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_notableclient(self, notableclient: NotableClient) -> NotableClient:
        async with self.db:
            async with self.db.session as session:
                session.add(notableclient)
                await session.commit()
                await session.refresh(notableclient)
                return notableclient

    async def update_notableclient(self, notableclientId: str, updatedNotableClient: dict) -> NotableClient:
        async with self.db:
            async with self.db.session as session:
                notableclient = await session.get(NotableClient, notableclientId)
                if not notableclient:
                    raise Exception("NotableClient not found")
                for key, value in updatedNotableClient.items():
                    if value and hasattr(notableclient, key):
                        setattr(notableclient, key, value)
                session.add(notableclient)
                await session.commit()
                await session.refresh(notableclient)
                return notableclient

    async def delete_notableclient(self, notableclientId: str) -> str:
        async with self.db:
            async with self.db.session as session:
                notableclient = await session.get(NotableClient, notableclientId)
                if not notableclient:
                    raise Exception("NotableClient not found")
                session.delete(notableclient)
                await session.commit()
                return f"NotableClient {notableclientId} deleted"

    async def get_notableclient_by_id(self, notableclientId: str) -> NotableClient:
        async with self.db:
            async with self.db.session as session:
                notableclient = await session.get(NotableClient, notableclientId)
                if not notableclient:
                    raise Exception("NotableClient not found")
                return notableclient

    async def get_all_notableclients(self) -> list[NotableClient]:
        async with self.db:
            async with self.db.session as session:
                statement = select(NotableClient)
                result = await session.execute(statement)
                return result.scalars().all()

    async def get_notableclient_by_name(self, name: str) -> NotableClient:
        async with self.db:
            async with self.db.session as session:
                statement = select(NotableClient).where(NotableClient.client_name == name)
                result = await session.execute(statement)
                return result.scalar_one_or_none()