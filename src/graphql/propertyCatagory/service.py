from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.PropertyCatagories import PropertyCatagories
from src.models.repository.PropertyCatagoryRepository import PropertyCatagoriesRepository
from src.graphql.propertyCatagoryRelationship.services import PropertyCatagoryRelationService
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    CustomException, InternalServerErrorException, NotFoundException
)

class PropertyCatagoryService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.catagory_repo = PropertyCatagoriesRepository(self.db)
        self.property_service = PropertyCatagoryRelationService(self.db)
    
    async def create_catagory(self, catagory: Dict) -> PropertyCatagories:
        try:
            if await self.get_catagory_by_name(catagory.get("name")):
                raise CustomException(status_code=409,detail="Catagory already exists")
            
            return await self.catagory_repo.create_catagory(PropertyCatagories(**catagory))
        except CustomException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def update_catagory(self, catagory_id: str, catagory_data: Dict) -> PropertyCatagories:
        try:
            if await self.get_catagory_by_name(catagory_data.get("name")):
                raise CustomException(status_code=409,detail="Catagory already exists, Cancel the update")
            
            return await self.catagory_repo.update_catagory(catagory_id, catagory_data)
        except CustomException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_catagory(self, catagory_id: str) -> PropertyCatagories:
        try:
            category = await self.catagory_repo.get_catagory(catagory_id)
            if not category:
                raise NotFoundException(detail="Catagory not found")
            return category
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
        
    async def get_catagory_by_name(self, name: str) -> PropertyCatagories:
        try:
            catagory = await self.catagory_repo.get_catagory_by_name(name)
            if not catagory:
                raise NotFoundException(detail="Catagory not found")
            return catagory
        except NotFoundException as w:
            raise w
        except Exception as e:
            raise InternalServerErrorException()
    
    async def delete_catagory(self, catagory_id: str) -> str:
        try:
            catagory_relation = await self.property_service.get_relation_by_catagory_id(catagory_id)
            if catagory_relation:
                raise CustomException(status_code=409, detail="Catagory has a relationship with a property, Cannot delete")
            return await self.catagory_repo.delete_catagory(catagory_id)
        except CustomException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
        