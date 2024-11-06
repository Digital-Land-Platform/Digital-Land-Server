import strawberry
from uuid import UUID
from .services import ImageService 
from src.graphql.image.types import ImageInput, ImageUpdateInput, ImageTypes
from config.database import db
from typing import List, Optional
from fastapi import UploadFile
from strawberry.file_uploads import Upload
import logging

image_service = ImageService(db.SessionLocal())

@strawberry.type
class ImageMutation:
    @strawberry.mutation
    async def create_image(self, image_input: ImageInput) -> ImageTypes:
        return await image_service.create_image(image_input)
    
    @strawberry.mutation
    async def update_image(self, image_update_input: ImageUpdateInput) -> ImageTypes:
        updated_image = await image_service.update_image(image_update_input)
        if updated_image:
            return ImageType(id=updated_image.id, url=updated_image.url, property_id=updated_image.property_id)
        else:
            raise Exception("Failed to update image")

    @strawberry.mutation
    async def delete_image(self, image_ids: List[UUID]) -> bool:
        return await image_service.delete_image(image_ids)
