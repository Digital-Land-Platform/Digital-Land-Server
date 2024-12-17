from src.models.Certification import Certification
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class CertificationRepository:
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_certification(self, certification: Certification) -> Certification:
        async with self.db:
            async with self.db.session as session:
                session.add(certification)
                await session.commit()
                await session.refresh(certification)
                return certification
    
    async def update_certification(self, certificationId: str, updatedCertification: dict) -> Certification:
        async with self.db:
            async with self.db.session as session:
                certification = await session.get(Certification, certificationId)
                if not certification:
                    raise Exception("Certification not found")
                for key, value in updatedCertification.items():
                    if value and hasattr(certification, key):
                        setattr(certification, key, value)
                session.add(certification)
                await session.commit()
                await session.refresh(certification)
                return certification
    
    async def delete_certification(self, certificationId: str) -> str:
        async with self.db:
            async with self.db.session as session:
                certification = await session.get(Certification, certificationId)
                if not certification:
                    raise Exception("Certification not found")
                session.delete(certification)
                await session.commit()
                return f"Certification {certificationId} deleted"
    
    async def get_certification_by_id(self, certificationId: str) -> Certification:
        async with self.db:
            async with self.db.session as session:
                certification = await session.get(Certification, certificationId)
                if not certification:
                    raise Exception("Certification not found")
                return certification
    
    async def get_all_certifications(self) -> list[Certification]:
        async with self.db:
            async with self.db.session as session:
                statement = select(Certification)
                certifications = await session.execute(statement)
                return certifications.scalars().all()

    async def get_certification_by_name(self, certificationName: str) -> Certification:
        async with self.db:
            async with self.db.session as session:
                statement = select(Certification).where(Certification.certification_name == certificationName)
                result = await session.execute(statement)
                certification = result.scalars().first()
                return certification
            