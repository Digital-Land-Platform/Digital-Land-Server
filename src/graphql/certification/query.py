from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
import strawberry
import strawberry.exceptions
from .types import CertificationType, CertificationBaseInput
from .service import CertificationService
from config.database import db

certefication_service = CertificationService(db)
@strawberry.type
class CertificationQuery:

    @strawberry.field
    async def get_certification(self, info, certification_id: str) -> CertificationType:
        try:
            certification = await certefication_service.get_certification(certification_id)
            return CertificationType.from_model(certification)
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)
    
    @strawberry.field
    async def get_all_certifications(self, info) -> List[CertificationType]:
        try:
            certifications = await certefication_service.get_all_certifications()
            return [CertificationType.from_model(certification) for certification in certifications]
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)