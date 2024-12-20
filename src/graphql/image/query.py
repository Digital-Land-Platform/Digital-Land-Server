import strawberry
from uuid import UUID
from typing import List, Optional
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .types import ImageTypes 
from .services import ImageService  
from config.database import db

service = ImageService(db)
@strawberry.type
class ImageQuery:
    @strawberry.field
    @ExceptionHandler.handle_exceptions
    async def get_image(self, image_id: UUID) -> Optional[ImageTypes]:
        return await service.get_image_by_id(image_id)

    @strawberry.field
    @ExceptionHandler.handle_exceptions
    async def list_images(self, property_id: UUID) -> List[ImageTypes]:
        return await service.list_images_by_property(property_id)
