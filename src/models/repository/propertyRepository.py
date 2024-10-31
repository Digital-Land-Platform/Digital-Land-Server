from uuid import UUID
from typing import Optional, List
from sqlalchemy.future import select
from src.models.Property import Property
from src.models.Image import Image
from src.models.Amenities import Amenities
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from config.database import DatabaseSession
from config.database import db


class PropertyRepository:
    def __init__(self, db: AsyncSession):
        """
        Initializes the property repository with the database session.
    
        Args:
            db (AsyncSession): The database session.
        """
        self.db = db

    async def create_property(
        self,
        new_property: Property
    ) -> Property:
        """
        Create a new property in the database.
        
        Args:
            new_property (Property): The property object to be created.
            
        Returns:
            Property: The created property object.
        """
        
        self.db.add(new_property)
        await self.db.commit()
        return new_property

     
    async def get_existing_property(self, title: str, location: str, user_id: UUID):
        """
        Get an existing property from the database.
        """
        async with self.db:
            result = await self.db.execute(
                select(Property).where(
                    func.lower(Property.title) == func.lower(title),
                    func.lower(Property.location) == func.lower(location),
                    Property.owner_id == user_id
                )
            )
            return result.scalar()


    async def update_property(
        self,
        property_: Property
    ) -> Optional[Property]:
        """
        Update a property in the database.
        
        Args:
            property_ (Property): The property object to be updated.
            
        Returns:
            Optional[Property]: The updated property object.
        """

        self.db.add(property_)
        await self.db.commit()
        return property_


    async def get_property(self, id: UUID) -> Optional[Property]:
        """
        Get a property by ID.
        
        Args:
        
            id (UUID): The ID of the property to be fetched.
            
        Returns:
        
            Optional[Property]: The property object.
        """
        async with self.db as session:
            result = await session.execute(
                select(Property)
                .options(joinedload(Property.images), joinedload(Property.amenities))
                .where(Property.id == id)
            )
            return result.unique().scalar_one_or_none()
        
    async def delete_property(self, id: UUID) -> bool:
        """
        Delete a property.
        
        Args:
            id (UUID): The ID of the property to be deleted.
            
        Returns:
        
            bool: True if the property was deleted successfully, False otherwise.
            
        """
        async with self.db:
            property_ = await self.db.get(Property, id)
            if property_:
                await self.db.delete(property_)
                await self.db.commit()
                return True
            return False

    async def list_properties(self):
        """
        List all properties.
        
        Returns:
            list[Property]: A list of all properties
        """
        async with self.db as session:
            result = await session.execute(
                select(Property)
                .options(joinedload(Property.images), joinedload(Property.amenities)) 
            )
            properties = result.scalars().unique()
            return properties.all() if result else None 
        
    
        
    

