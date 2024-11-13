from typing import Dict
from src.models import Certification
from src.models.repository.CertificationRepository import CertificationRepository
from sqlalchemy.ext.asyncio import AsyncSession

class CertificationService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.certification_repository = CertificationRepository(db)
    
    async def create_certification(self, certification_input: Dict) -> Certification:
        try:
            print("certification_input", certification_input)
            check = await self.certification_repository.get_certification_by_name(certification_input["certification_name"])
            if check:
                raise Exception("Certification already exists")
            certification = Certification(**certification_input)
            return await self.certification_repository.create_certification(certification)
        except Exception as e:
            raise Exception(f"Failed to create certification: {e}")\
    
    async def update_certification(self, certification_id: str, updated_certification: dict) -> Certification:
        try:
            return await self.certification_repository.update_certification(certification_id, updated_certification)
        except Exception as e:
            raise Exception(f"Failed to update certification: {e}")
        
    async def get_certification(self, certification_id: str) -> Certification:
        try:
            return await self.certification_repository.get_certification_by_id(certification_id)
        except Exception as e:
            raise Exception(f"Failed to fetch certification: {e}")
    
    async def get_all_certifications(self) -> list[Certification]:
        try:
            return await self.certification_repository.get_all_certifications()
        except Exception as e:
            raise Exception(f"Failed to fetch certifications: {e}")
    
    async def delete_certification(self, certification_id: str) -> str:
        try:
            return await self.certification_repository.delete_certification(certification_id)
        except Exception as e:
            raise Exception(f"Failed to delete certification: {e}")