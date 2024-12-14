from typing import Dict, List
from src.models import Certification
from src.models.repository.CertificationRepository import CertificationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException,
    NotFoundException,
    InternalServerErrorException,
    CustomException,
)

class CertificationService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.certification_repository = CertificationRepository(db)
    
    async def create_certification(self, certification_input: Dict) -> Certification:
        try:
            check = await self.certification_repository.get_certification_by_name(certification_input["certification_name"])
            if check:
                raise CustomException(status_code=409, detail="Certification already exists")
            certification = Certification(**certification_input)
            return await self.certification_repository.create_certification(certification)
        except CustomException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def update_certification(self, certification_id: str, updated_certification: Dict) -> Certification:
        try:
            return await self.certification_repository.update_certification(certification_id, updated_certification)
        except Exception as e:
            raise InternalServerErrorException()
        
    async def get_certification(self, certification_id: str) -> Certification:
        try:
            certification = await self.certification_repository.get_certification_by_id(certification_id)
            if not certification:
                raise NotFoundException(detail="Certification not found")
            return certification
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_all_certifications(self) -> List[Certification]:
        try:
            certificates = await self.certification_repository.get_all_certifications()
            if not certificates:
                raise NotFoundException(detail="No certifications found")
            return certificates
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def delete_certification(self, certification_id: str) -> str:
        try:
            result = await self.certification_repository.delete_certification(certification_id)
            if not result:
                raise NotFoundException(detail="Certification not found")
            return result
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()