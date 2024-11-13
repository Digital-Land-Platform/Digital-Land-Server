from typing import Optional
from fastapi import HTTPException
from .types import NotableClientInput, NotableClientType, NotableClientInput
from .service import NotableClientService
from config.database import db
import strawberry

notableclient_service = NotableClientService(db)

@strawberry.type
class NotableClientMutation:
    
    @strawberry.mutation
    async def create_notableclient(self, info, notableclient_input: NotableClientInput) -> NotableClientType:
        try:
            if notableclient_input:
                notableclient_value = vars(notableclient_input)
                notableclient = await notableclient_service.create_notableclient(notableclient_value)
                return NotableClientType.from_model(notableclient)
            else:
                return None
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)

    @strawberry.mutation
    async def update_notableclient(self, info, notableclient_id: str, notableclient: NotableClientInput) -> NotableClientType:
        try:
            if notableclient:
                notableclient_value = vars(notableclient)
                updated_notableclient = await notableclient_service.update_notableclient(notableclient_id, notableclient_value)
                return NotableClientType.from_model(updated_notableclient)
            else:
                return None
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)

    @strawberry.mutation
    def delete_notableclient(info, notableclient_id: str) -> Optional[str]:
        try:
            return notableclient_service.delete_notableclient(notableclient_id)
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)