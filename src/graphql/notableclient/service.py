from src.middleware.ErrorHundlers.CustomErrorHandler import (
    CustomException, InternalServerErrorException, NotFoundException
)
from src.models.repository.NotableClientRepository import NotableClientRepository
from typing import Dict
from src.models.NotableClient import NotableClient
from sqlalchemy.ext.asyncio import AsyncSession

class NotableClientService:
     
    def __init__(self, db: AsyncSession):
        self.db = db
        self.notableclient_repository = NotableClientRepository(db)
    
    async def create_notableclient(self, notableclient_input: Dict) -> NotableClient:
        try:
            check = await self.notableclient_repository.get_notableclient_by_name(notableclient_input["client_name"])
            if check:
                raise CustomException(status_code=409, detail="NotableClient already exists")
            notableclient = NotableClient(**notableclient_input)
            return await self.notableclient_repository.create_notableclient(notableclient)
        except CustomException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def update_notableclient(self, notableclient_id: str, updated_notableclient: dict) -> NotableClient:
        try:
            client = await self.notableclient_repository.get_notableclient_by_id(notableclient_id)
            if not client:
                raise NotFoundException(detail="NotableClient not found")
            
            return await self.notableclient_repository.update_notableclient(notableclient_id, updated_notableclient)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
        
    async def get_notableclient(self, notableclient_id: str) -> NotableClient:
        try:
            return await self.notableclient_repository.get_notableclient_by_id(notableclient_id)
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_all_notableclients(self) -> list[NotableClient]:
        try:
            return await self.notableclient_repository.get_all_notableclients()
        except Exception as e:
            raise InternalServerErrorException()
    
    async def delete_notableclient(self, notableclient_id: str) -> str:
        try:
            client = await self.notableclient_repository.get_notableclient_by_id(notableclient_id)
            if not client:
                raise NotFoundException(detail="Notable Client not found")
        
            return await self.notableclient_repository.delete_notableclient(notableclient_id)
        except Exception as e:
            raise InternalServerErrorException()
        