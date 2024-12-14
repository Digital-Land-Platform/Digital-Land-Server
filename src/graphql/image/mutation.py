import strawberry
from uuid import UUID
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from src.graphql.property.types import ImageType
from .services import ImageService 
from src.graphql.image.types import ImageInput, ImageUpdateInput, ImageTypes
from config.database import db
from src.middleware.AuthManagment import AuthManagement
from typing import List, Optional
from fastapi import UploadFile
from strawberry.file_uploads import Upload
import logging

auth_management = AuthManagement()
image_service = ImageService(db.SessionLocal())

@strawberry.type
class ImageMutation:
    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def create_image(self, image_input: ImageInput) -> ImageTypes:
        return await image_service.create_image(image_input)
    
    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def update_image(self, image_update_input: ImageUpdateInput) -> ImageTypes:
        updated_image = await image_service.update_image(image_update_input)
        if updated_image:
            return ImageType(id=updated_image.id, url=updated_image.url, property_id=updated_image.property_id)
        else:
            raise Exception("Failed to update image")

    @strawberry.mutation
    @ExceptionHandler.handle_exceptions
    async def delete_image(self, image_ids: List[UUID]) -> bool:
        return await image_service.delete_image(image_ids)
