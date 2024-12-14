import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .types import MessageTypes
from .services import MessageService
from typing import List
from config.database import db
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole


auth_management = AuthManagement()
message_service = MessageService(db)

@strawberry.type
class MessageQuery:

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_conversation(self, info, user_id: str) -> List[MessageTypes]:
        messages = await message_service.get_conversation(user_id)
        return [MessageTypes.from_orm(message) for message in messages]
    
    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_conversation_users(self, info, user1: str, user2: str) -> List[MessageTypes]:
        messages = await message_service.get_conversation_users(user1, user2)
        return [MessageTypes.from_orm(message) for message in messages]
    
    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_message_by_id(self, info, message_id: str) -> MessageTypes:
        message = await message_service.get_message(message_id)
        return MessageTypes.from_orm(message)

    @strawberry.field
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def get_recent_conversation(self, info, user_id: str) -> List[MessageTypes]:
        messages = await message_service.get_recent_conversations(user_id)
        return [MessageTypes.from_orm(message) for message in messages]