from src.models.Certification import Certification
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class CertificationRepository:
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_certification(self, certification: Certification) -> Certification:
        try:
            async with self.db:
                async with self.db.session as session:
                    session.add(certification)
                    await session.commit()
                    await session.refresh(certification)
                    return certification
        except Exception as e:
            raise Exception(f"Failed to create certification: {e}")
    
    async def update_certification(self, certificationId: str, updatedCertification: dict) -> Certification:
        try:
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
        except Exception as e:
            raise Exception(f"Failed to update certification: {e}")
    
    async def delete_certification(self, certificationId: str) -> str:
        try:
            async with self.db:
                async with self.db.session as session:
                    certification = await session.get(Certification, certificationId)
                    if not certification:
                        raise Exception("Certification not found")
                    session.delete(certification)
                    await session.commit()
                    return f"Certification {certificationId} deleted"
        except Exception as e:
            raise Exception(f"Failed to delete certification: {e}")
    
    async def get_certification_by_id(self, certificationId: str) -> Certification:
        try:
            async with self.db:
                async with self.db.session as session:
                    certification = await session.get(Certification, certificationId)
                    if not certification:
                        raise Exception("Certification not found")
                    return certification
        except Exception as e:
            raise Exception(f"Failed to get certification: {e}")
    
    async def get_all_certifications(self) -> list[Certification]:
        try:
            async with self.db:
                async with self.db.session as session:
                    statement = select(Certification)
                    certifications = await session.execute(statement)
                    return certifications.scalars().all()
        except Exception as e:
            raise Exception(f"Failed to get certifications: {e}")

    async def get_certification_by_name(self, certificationName: str) -> Certification:
        try:
            async with self.db:
                async with self.db.session as session:
                    statement = select(Certification).where(Certification.certification_name == certificationName)
                    result = await session.execute(statement)
                    certification = result.scalars().first()
                    return certification
        except Exception as e:
            raise Exception(f"Failed to get certification: {e}")    