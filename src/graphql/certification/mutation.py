from typing import Optional
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
import strawberry
import strawberry.exceptions
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from src.middleware.AuthManagment import AuthManagement
from .types import CertificationType, CertificationBaseInput
from .service import CertificationService
from config.database import db

auth_management = AuthManagement()
certefication_service = CertificationService(db)


@strawberry.type
class CertificationMutation:
    
    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def create_certification(self, info, certification_input: CertificationBaseInput) -> CertificationType:
        if certification_input:
            certification_value = vars(certification_input)
            certification = await certefication_service.create_certification(certification_value)
            return CertificationType.from_model(certification)
        else:
            return None

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def update_certification(self, info, certification_id: str, certification: CertificationBaseInput) -> CertificationType:
        if certification:
            certification_value = vars(certification)
            updated_certification = await certefication_service.update_certification(certification_id, certification_value)
            return CertificationType.from_model(updated_certification)
        else:
            return None

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    def delete_certification(info, certification_id: str) -> Optional[str]:
        return certefication_service.delete_certification(certification_id)
