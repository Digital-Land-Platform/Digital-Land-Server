from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.Amenity import Amenity as Amenities


class AmenityRepository:
    def __init__(self, db: AsyncSession):
        """
        Initializes the property repository with the database session.
    
        Args:
            db (AsyncSession): The database session.
        """
        self.db = db
    async def create_amenity(self, amenity_data: Amenities) -> Amenities:
        """
        Create a new amenity in the database.

        Args:
            amenity (Amenities): The amenity object to be created.

        Returns:
            Amenities: The created amenity object.
        """
        self.db.add(amenity_data)
        await self.db.commit()
        return amenity_data
    
    async def update_amenity(self, amenity: Amenities) -> Amenities:
        """
        Update an existing amenity in the database.

        Args:
            amenity_data (Amenities): The amenity object with updated data.

        Returns:
            Amenities: The updated amenity object.
        """
        async with self.db as session:
            session.add(amenity)  
            await session.commit()  
            return amenity  
    
    async def get_amenities_by_ids(self, amenity_ids: List[UUID]) -> List[Amenities]:
        """
        Fetch amenities by their IDs.

        Args:
            amenity_ids (List[UUID]): The list of amenity IDs to fetch.

        Returns:
            List[Amenities]: A list of found amenities.
        """
        async with self.db as session:
            result = await session.execute(
                select(Amenities).where(Amenities.id.in_(amenity_ids))
            )
            return result.scalars().all() if result else []
        
    async def delete_amenity(self, amenity_id: UUID) -> bool:
        """
        Delete an amenity from the database.

        Args:
            amenity_id (UUID): The ID of the amenity to delete.

        Returns:
            bool: True if the amenity was deleted successfully, False otherwise.
        """
        async with self.db as session:
                result = await session.execute(
                    select(Amenities).where(Amenities.id == amenity_id)
                )
                amenity = result.scalars().first()
                
                if amenity:
                    await session.delete(amenity)
                    await session.commit()  
                    return True
                return False
             
            
    async def get_amenity_by_title(self, title: str) -> Optional[Amenities]:
        """
        Fetch an amenity by its title from the database.
        """
        
        async with self.db as session:
            result = await session.execute(
                select(Amenities).where(Amenities.title == title)
            )
            return result.scalars().first()
    
    
    async def get_amenity_by_id(self, amenity_id: UUID) -> Optional[Amenities]:
        """
        Fetch an amenity by its ID from the database.

        Args:
        amenity_id (UUID): The ID of the amenity to retrieve.

        Returns:
            Optional[Amenities]: The amenity object if found, else None.
        """
        async with self.db as session:
            result = await session.execute(
                select(Amenities).where(Amenities.id == amenity_id)
            )
            amenity = result.scalar_one_or_none()  
        return amenity
    
    async def get_all_amenities(self) -> List[Amenities]:
        """
        Retrieve all amenities from the database.
        
        Returns:
            List[Amenities]: A list of all amenities.
        """
        async with self.db as session:
            result = await session.execute(select(Amenities))
            return result.scalars().all()