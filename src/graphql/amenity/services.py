import strawberry
from uuid import UUID
from typing import Optional, List
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
        existing_amenity = await self.repository.get_amenity_by_title(amenity_data.title)
        if existing_amenity:
            raise Exception(f"Amenity '{amenity_data.title}' already exists.")
        return await self.repository.create_amenity(amenity_data)
    
    async def update_amenity(self, amenity_id: UUID, amenity_update_input: AmenityUpdateInput) -> Optional[Amenities]:
        """
        Update an existing amenity in the database.

        Args:
            amenity_id (UUID): The ID of the amenity to update.
            amenity_update_input (AmenityInput): The updated details for the amenity.

        Returns:
            Optional[Amenities]: The updated amenity.
        """
        amenity = await self.repository.get_amenity_by_id(amenity_id)
        
        if not amenity:
            raise Exception("Amenity not found")

        if amenity_update_input.title is not None:
            amenity.title = amenity_update_input.title
        if amenity_update_input.icon is not None:
            amenity.icon = amenity_update_input.icon

        return await self.repository.update_amenity(amenity)

    async def delete_amenity(self, amenity_id: UUID) -> bool:
        """
        Delete an existing amenity from the database.

        Args:
            amenity_id (UUID): The ID of the amenity to delete.

        Returns:
            bool: True if the amenity was deleted successfully, False otherwise.
        """
        
        return await self.repository.delete_amenity(amenity_id)
    
    async def list_all_amenities(self):
        """
        List all amenities.
        
        Returns:
            List[Amenities]: A list of all amenities.
        """
        return await self.repository.get_all_amenities()
    
    async def get_amenity_by_id(self, amenity_id: UUID):
        """
        Retrieve a single amenity by its ID.

        Args:
            amenity_id (UUID): The ID of the amenity to retrieve.

        Returns:
            Optional[Amenities]: The amenity if found, else None.
        """
        return await self.repository.get_amenity_by_id(amenity_id)