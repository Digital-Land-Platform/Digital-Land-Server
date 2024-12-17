from sqlalchemy import and_, func, or_, select
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.Message import Message
from sqlalchemy.orm import aliased

class MessageRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(self, new_message: Message) -> Message:
        async with self.db:
            async with self.db.session as session:
                session.add(new_message)
                await session.commit()
                await session.refresh(new_message)
                return new_message
    
    async def update_message(self, message_id: str, message_data: Dict) -> Message:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Message).where(Message.id == message_id)
                )
                message = result.scalar_one_or_none()
                for key, value in message_data.items():
                    if value and hasattr(message, key):
                        setattr(message, key, value)
                    else:
                        raise Exception(f"Invalid message data: {key}")
                await session.commit()
                await session.refresh(message)
                return message
    
    async def delete_message(self, message_id: str) -> str:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Message).where(Message.id == message_id)
                )
                message = result.scalar().first()
                await session.delete(message)
                await session.commit()
                return f"Message {message_id} deleted"

    async def get_message(self, message_id: str) -> Message:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Message).where(Message.id == message_id)
                )
                return result.scalar_one_or_none()
    
    async def get_conversasion(self, user_id: str) -> List[Message]:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Message).where(
                         or_(
                            Message.sender_id == user_id,
                            Message.receiver_id == user_id
                        )
                    ).order_by(Message.sent_at.desc())
                )
                return result.scalars().all()
    
    async def get_conversation_users(self, user1: str, user2: str) -> List[Message]:
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Message).where(
                        or_(
                            and_(Message.sender_id == user1, Message.receiver_id == user2),
                            and_(Message.sender_id == user2, Message.receiver_id == user1)
                        )
                    ).order_by(Message.sent_at.desc())
                )
                return result.scalars().all()
    
    async def get_recent_conversations(self, user_id: str):
        async with self.db:
            async with self.db.session as session:
                # Get the most recent message for each conversation (grouped by user pairs)
                subquery = (
                    select(
                        func.max(Message.sent_at).label("latest_sent_at"),
                        func.least(Message.sender_id, Message.receiver_id).label("user1"),
                        func.greatest(Message.sender_id, Message.receiver_id).label("user2")
                    )
                    .where(or_(Message.sender_id == user_id, Message.receiver_id == user_id))
                    .group_by("user1", "user2")
                    .subquery()
                )

                # Alias the Message table
                msg_alias = aliased(Message)

                # Join with subquery to get the most recent message for each conversation
                query = (
                    select(msg_alias)
                    .join(
                        subquery,
                        and_(
                            func.least(msg_alias.sender_id, msg_alias.receiver_id) == subquery.c.user1,
                            func.greatest(msg_alias.sender_id, msg_alias.receiver_id) == subquery.c.user2,
                            msg_alias.sent_at == subquery.c.latest_sent_at
                        )
                    )
                    .order_by(msg_alias.sent_at.desc())
                )

                # Execute the query
                result = await session.execute(query)
                return result.scalars().all()