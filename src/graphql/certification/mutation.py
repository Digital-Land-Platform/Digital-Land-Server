from typing import Optional
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
import strawberry
import strawberry.exceptions
from .types import CertificationType, CertificationBaseInput
from .service import CertificationService
from config.database import db

certefication_service = CertificationService(db)


@strawberry.type
class CertificationMutation:
    
    @strawberry.mutation
    async def create_certification(self, info, certification_input: CertificationBaseInput) -> CertificationType:
        try:
            if certification_input:
                certification_value = vars(certification_input)
                certification = await certefication_service.create_certification(certification_value)
                return CertificationType.from_model(certification)
            else:
                return None
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)

    @strawberry.mutation
    async def update_certification(self, info, certification_id: str, certification: CertificationBaseInput) -> CertificationType:
        try:
            if certification:
                certification_value = vars(certification)
                updated_certification = await certefication_service.update_certification(certification_id, certification_value)
                return CertificationType.from_model(updated_certification)
            else:
                return None
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)

    @strawberry.mutation
    def delete_certification(info, certification_id: str) -> Optional[str]:
        try:
            return certefication_service.delete_certification(certification_id)
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)