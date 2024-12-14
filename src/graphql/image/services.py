from uuid import UUID
from typing import Optional, List, Union
import cloudinary.uploader
from src.models.repository.ImageRepository import ImageRepository
from src.models.Image import Image
from src.graphql.image.types import ImageInput, ImageUpdateInput, ImageTypes
from config.database import db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException
from strawberry.file_uploads import Upload
from config.config import Config
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException,
    NotFoundException,
    InternalServerErrorException
)

cloudinary.config(
    cloud_name=Config.get_env_variable("CLOUDINARY_NAME"),
    api_key=Config.get_env_variable("CLOUDINARY_API_KEY"),
    api_secret=Config.get_env_variable("CLOUDINARY_API_SECRET")
)

class ImageService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = ImageRepository(db)

    async def create_image(self, image_input: ImageInput, property_id: UUID) -> Image:
        """
        Creates an image entry in the database after uploading to Cloudinary.
        Supports both URL-based and file-based image uploads.
        
        Args:
            image_input (ImageInput): The image data, which can include a URL or a file.

        Returns:
            Image: The created Image instance with a Cloudinary URL.
        """
        try:
            image_url = None
            
            if image_input.file:
                file_content = await image_input.file.read()
                # Upload the file to Cloudinary
                upload_result = cloudinary.uploader.upload(file_content, resource_type='image')
                image_url = upload_result['secure_url']
            elif image_input.url:
                # Upload the URL to Cloudinary
                upload_result = cloudinary.uploader.upload(image_input.url, resource_type='image')
                image_url = upload_result['secure_url']
            else:
                raise BadRequestException(detail="Either a file or a URL is required")

            # Create Image instance with the Cloudinary URL
            image = Image(
                url=image_url,
                property_id=property_id
            )
            return await self.repository.create_image(image)
        except BadRequestException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException(detail=f"Error creating image: {e}")

    async def update_image(self, image_update_input: ImageUpdateInput) -> Optional[Image]:
        """
        Updates an image in the database and Cloudinary.
        
        Args:
            image_update_input (ImageUpdateInput): The image data to update.
            
        Returns:
            Optional[Image]: The updated image instance.
        """
        try:
            image = await self.repository.get_image_by_id(image_update_input.image_id)
            
            if not image:
                raise NotFoundException(detail="Image not found")
            
            public_id = image.url.split('/')[-1].split('.')[0]
            cloudinary.uploader.destroy(public_id)
            # Upload new image to Cloudinary if file is provided
            if image_update_input.file is not None:
                file_content = await image_update_input.file.read()
                upload_result = cloudinary.uploader.upload(file_content, resource_type='image')
                image.url = upload_result['secure_url']
                
            return await self.repository.update_image(image)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException(detail=f"Error updating image: {e}")

    async def delete_image(self, image_ids: List[UUID]) -> bool:
        """
        Deletes an image from the database and Cloudinary.
        
        Args:
            image_id (UUID): The ID of the image to delete.
            
        Returns:
            bool: True if the image was successfully deleted.
        """
        try:
            for image_id in image_ids:
                image = await self.repository.get_image_by_id(image_id) 
                if not image:
                    raise NotFoundException(detail="Image not found")
            
                # Delete from Cloudinary
                public_id = image.url.split('/')[-1].split('.')[0]  
                cloudinary.uploader.destroy(public_id)
            
                await self.repository.delete_image(image_id)
            return True
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException(detail=f"Error deleting image: {e}")
    
    async def get_image_by_id(self, image_id: UUID) -> Optional[Image]:
        """
        Get an image by ID
        Args:
            image_id (UUID): Image ID
        Returns:
            Optional[Image]: The image instance
        """
        try:
            image = await self.repository.get_image_by_id(image_id)
            if not image:
                raise NotFoundException(detail="Image not found")
            return image
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException(detail=f"Error fetching image: {e}")

    async def list_images_by_property(self, property_id: UUID) -> List[Image]:
        """
        List images by property ID
        Args:
            property_id (UUID): Property ID
        Returns:
            List[Image]: List of images
        """
        try:
            return await self.repository.get_images_by_property(property_id)
        except Exception as e:
            raise InternalServerErrorException(detail=f"Error fetching images: {e}")