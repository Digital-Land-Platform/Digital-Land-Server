from datetime import datetime
from typing import Dict
from src.middleware.ErrorHundlers.CustomErrorHandler import InternalServerErrorException
from src.models.repository.MessageRepository import MessageRepository
from src.models.Message import Message
from src.models.enums.MessageStatus import MessageStatus
from src.graphql.users.services import UserService
from src.graphql.property.services import PropertyService
from sqlalchemy.ext.asyncio import AsyncSession
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException,
    NotFoundException,
    InternalServerErrorException
)

class MessageService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.message_repo = MessageRepository(self.db)
        self.user_service = UserService(self.db)
        self.property_service = PropertyService(self.db)
    
    async def create_message(self, new_message: Dict) -> Message:
        try:
            if "status" in new_message and new_message.get("status"):
                status_name = new_message.get("status").name
                new_message["status"] = getattr(MessageStatus, status_name, None)
                if new_message["status"] is None:
                    raise BadRequestException(f"Invalid status: {status_name}")
            sender = await self.user_service.get_user_by_id(new_message.get("sender_id"))
            if not sender:
                raise NotFoundException("Sender not found")
            reciever = await self.user_service.get_user_by_id(new_message.get("receiver_id"))
            if not reciever:
                raise NotFoundException("User not found")
            if new_message.get("property_id"):
                property = await self.property_service.get_property(new_message.get("property_id"))
                if not property:
                    raise NotFoundException("Property not found")
            if not new_message.get("sent_at"):
                new_message["sent_at"] = datetime.now()
            message = await self.message_repo.create_message(Message(**new_message))
            return message
        except (BadRequestException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def update_message(self, message_id: str, message_data: Dict) -> Message:
        try:
            message = await self.message_repo.get_message_by_id(message_id)
            if not message:
                raise NotFoundException(detail="Message not found")

            if "status" in message_data and message_data.get("status"):
                status_name = message_data.get("status").name
                message_data["status"] = getattr(MessageStatus, status_name, None)
                if message_data["status"] is None:
                    raise BadRequestException(detail="Invalid status")

            return await self.message_repo.update_message(message_id, message_data)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def delete_message(self, message_id: str) -> str:
        try:
            message = await self.message_repo.get_message_by_id(message_id)
            if not message:
                raise NotFoundException(detail="Message not found")
            
            await self.message_repo.delete_message(message_id)
            return True
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()

    async def get_conversation(self, user_id: str) -> list:
        try:
            user = await self.user_service.get_user_by_id(user_id)
            if not user:
                raise NotFoundException("User not found")
            
            return await self.message_repo.get_conversasion(user_id)
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_conversation_users(self, user1: str, user2: str) -> list:
        try:
            return await self.message_repo.get_conversation_users(user1, user2)
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_message(self, message_id: str) -> Message:
        try:
            message = await self.message_repo.get_message_by_id(message_id)
            if not message:
                raise NotFoundException(detail="Message not found")
        
            return await self.message_repo.get_message(message_id)
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_recent_conversations(self, user_id: str) -> list:
        try:
            user = await self.user_service.get_user_by_id(user_id)
            if not user:
                raise NotFoundException("User not found")
            
            return await self.message_repo.get_recent_conversations(user_id)
        except Exception as e:
            raise InternalServerErrorException()
    

    
    