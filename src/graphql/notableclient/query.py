from typing import List
from fastapi import HTTPException
from .types import NotableClientType
from .service import NotableClientService
from config.database import db
import strawberry

notableclient_service = NotableClientService(db)

@strawberry.type
class NotableClientQuery:

    @strawberry.field
    async def get_notableclient(self, info, notableclient_id: str) -> NotableClientType:
        try:
            notableclient = await notableclient_service.get_notableclient(notableclient_id)
            return NotableClientType.from_model(notableclient)
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)
    
    @strawberry.field
    async def get_all_notableclients(self, info) -> List[NotableClientType]:
        try:
            notableclients = await notableclient_service.get_all_notableclients()
            return [NotableClientType.from_model(notableclient) for notableclient in notableclients]
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)