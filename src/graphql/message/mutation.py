import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .types import MessageTypes, MessageInput, UpdateMessageInput
from .services import MessageService
from typing import List
from config.database import db
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole


auth_management = AuthManagement()
message_service = MessageService(db)

@strawberry.type
class MessageMutation:

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def create_message(self, info, message_data: MessageInput) -> MessageTypes:
        message_data = vars(message_data)
        message = await message_service.create_message(message_data)
        return MessageTypes.from_orm(message)

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def update_message(self, info, message_id: str, message_data: UpdateMessageInput) -> MessageTypes:
        message_data = vars(message_data)
        message = await message_service.update_message(message_id, message_data)
        return MessageTypes.from_orm(message)
        
    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def delete_message(self, info, message_id: str) -> str:
        return  await message_service.delete_message(message_id)
