from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.Image import Image
from typing import Optional, List
from sqlalchemy.future import select

class ImageRepository:
    def __init__(self, db: AsyncSession):
        """
        Initializes the image repository with the database session.
    
        Args:
            db (AsyncSession): The database session.
        """
        self.db = db

    async def create_image(self, image: Image) -> Image:
        """
        Create a new image in the database.
        
        Args:
            image (Image): The image object to be created.
            
        Returns:
            Image: The created image object.
        """
        async with self.db as session:
            session.add(image)
            await self.db.commit()
            await self.db.refresh(image)
            return image

    async def get_image_by_id(self, image_id: UUID) -> Optional[Image]:
        """
        Get an image by ID.
        
        Args:
            image_id (UUID): The ID of the image to be fetched.
            
        Returns:
            Optional[Image]: The image object.
        """
        async with self.db as session:
            result = await session.execute(
                select(Image).where(Image.id == image_id)
            )
            return result.scalars().first()

    async def update_image(self, image: Image) -> Image:
        """
        Update an image in the database.
        
        Args:
            image (Image): The image object to be updated.
            
        Returns:
            Image: The updated image object.
        """
        self.db.add(image)  # Add the modified image instance
        await self.db.commit()    # Commit the changes
        await self.db.refresh(image)  # Refresh to get the latest data
        return image
    async def delete_image(self, image_id: List[UUID]) -> bool:
        """
        Delete an image by ID.
        
        Args:
            image_id (UUID): The ID of the image to be deleted.
            
        Returns:
            bool: True if the image was deleted successfully, False otherwise.
        """
        async with self.db as session:
            image = await session.get(Image, image_id)
            if image:
                await session.delete(image)
                await session.commit()
                return True
            return False

    async def get_images_by_property(self, property_id: UUID) -> List[Image]:
        """
        Get all images associated with a property.
        
        Args:
            property_id (UUID): The ID of the property.
            
        Returns:
            List[Image]: A list of image objects.
        """
        async with self.db as session:
            query = await session.execute(
                select(Image).where(Image.property_id == property_id)
            )
            return query.scalars().all()
