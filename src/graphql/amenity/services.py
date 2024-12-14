import strawberry
from uuid import UUID
from typing import Optional, List
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    CustomException, InternalServerErrorException, NotFoundException
)
from src.models.Amenity import Amenity as Amenities
from src.models.repository.AmenityRepository import AmenityRepository
from sqlalchemy.ext.asyncio import AsyncSession
from .types import AmenitiesType, AmenityInput, AmenityUpdateInput
class AmenityService:
    def __init__(self, db: AsyncSession):
        """
        initializes the property service with the database session
        
        Args:
            db (AsyncSession): the database session
        """
        self.db = db
        self.repository = AmenityRepository(db) 
    async def create_amenity(self, amenity_data: Amenities) -> Amenities:
        """
        Create a new amenity in the database.
        
        Args:
            amenity_data (Amenities): The amenity object to be created.
            
        Returns:
            Amenities: The created amenity object.
        """
        try:
            existing_amenity = await self.repository.get_amenity_by_title(amenity_data.title)
            if existing_amenity:
                raise CustomException(status_code=409, detail=f"Amenity called '{amenity_data.title}' already exists.")
            return await self.repository.create_amenity(amenity_data)
        except Exception as e:
            raise CustomException(status_code=500, detail="Error creating amenity.")
        except Exception as e:
            raise InternalServerErrorException()
    
    async def update_amenity(self, amenity_id: UUID, amenity_update_input: AmenityUpdateInput) -> Optional[Amenities]:
        """
        Update an existing amenity in the database.

        Args:
            amenity_id (UUID): The ID of the amenity to update.
            amenity_update_input (AmenityInput): The updated details for the amenity.

        Returns:
            Optional[Amenities]: The updated amenity.
        """
        try:
            amenity = await self.repository.get_amenity_by_id(amenity_id)
            
            if not amenity:
                raise NotFoundException("Amenity not found")

            if amenity_update_input.title is not None:
                amenity.title = amenity_update_input.title
            if amenity_update_input.icon is not None:
                amenity.icon = amenity_update_input.icon

            return await self.repository.update_amenity(amenity)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()

    async def delete_amenity(self, amenity_id: UUID) -> bool:
        """
        Delete an existing amenity from the database.

        Args:
            amenity_id (UUID): The ID of the amenity to delete.

        Returns:
            bool: True if the amenity was deleted successfully, False otherwise.
        """
        try:
            return await self.repository.delete_amenity(amenity_id)
        except Exception as e:
            raise InternalServerErrorException()
    
    async def list_all_amenities(self):
        """
        List all amenities.
        
        Returns:
            List[Amenities]: A list of all amenities.
        """
        try:
            return await self.repository.get_all_amenities()
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_amenity_by_id(self, amenity_id: UUID):
        """
        Retrieve a single amenity by its ID.

        Args:
            amenity_id (UUID): The ID of the amenity to retrieve.

        Returns:
            Optional[Amenities]: The amenity if found, else None.
        """
        try:
            return await self.repository.get_amenity_by_id(amenity_id)
        except Exception as e:
            raise InternalServerErrorException()   