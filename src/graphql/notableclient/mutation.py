import strawberry
from typing import Optional
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .types import NotableClientInput, NotableClientType, NotableClientInput
from .service import NotableClientService
from config.database import db
from src.middleware.AuthManagment import AuthManagement

auth_management = AuthManagement()
notableclient_service = NotableClientService(db)

@strawberry.type
class NotableClientMutation:
    
    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def create_notableclient(self, info, notableclient_input: NotableClientInput) -> NotableClientType:
        notableclient_value = vars(notableclient_input)
        notableclient = await notableclient_service.create_notableclient(notableclient_value)
        return NotableClientType.from_model(notableclient)

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def update_notableclient(self, info, notableclient_id: str, notableclient: NotableClientInput) -> NotableClientType:
        notableclient_value = vars(notableclient)
        updated_notableclient = await notableclient_service.update_notableclient(notableclient_id, notableclient_value)
        return NotableClientType.from_model(updated_notableclient)

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    def delete_notableclient(info, notableclient_id: str) -> Optional[str]:
        return notableclient_service.delete_notableclient(notableclient_id)
