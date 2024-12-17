from typing import List
import strawberry
import strawberry.exceptions
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .types import CertificationType
from .service import CertificationService
from config.database import db

certefication_service = CertificationService(db)
@strawberry.type
class CertificationQuery:

    @strawberry.field
    @ExceptionHandler.handle_exceptions
    async def get_certification(self, info, certification_id: str) -> CertificationType:
        certification = await certefication_service.get_certification(certification_id)
        return CertificationType.from_model(certification)
    
    @strawberry.field
    @ExceptionHandler.handle_exceptions
    async def get_all_certifications(self, info) -> List[CertificationType]:
        certifications = await certefication_service.get_all_certifications()
        return [CertificationType.from_model(certification) for certification in certifications]
    