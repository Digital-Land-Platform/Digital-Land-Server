from uuid import UUID
from typing import Optional
from sqlalchemy.future import select
from src.models.Property import Property
from config.database import DatabaseSession
from sqlalchemy import func

class PropertyRepository:
    def __init__(self):
        self.db = DatabaseSession()

    async def create_property(self, title: str, description: str, price: float, size: float,
                              location: str, neighborhood: str, city: str, country: str,
                              legalStatus: str, images: str, owner_id: UUID, status: str = "available"):
        """
        Create a new property.
        
        
        Args:
            title (str): The title of the property.
            description (str): The description of the property.
            price (float): The price of the property.
            size (float): The size of the property.
            location (str): The location of the property.
            neighborhood (str): The neighborhood of the property.
            city (str): The city of the property.
            country (str): The country of the property.
            legalStatus (str): The legal status of the property.
            images (str): The images of the property.
            owner_id (UUID): The owner ID of the property.
            status (str): The status of the property.
            
        Returns:
            Property: The newly created property object.
        """
        new_property = Property(
            title=title,
            description=description,
            price=price,
            size=size,
            location=location,
            neighborhood=neighborhood,
            city=city,
            country=country,
            owner_id=owner_id,
            status=status,
            images=images,
            legalStatus=legalStatus
        )
        async with self.db:
            async with self.db.session as session:
                session.add(new_property)
                await session.commit()
                await session.refresh(new_property)
        return new_property
    
    async def get_existing_property(self, title: str, location: str, owner_id: UUID):
        """
        Check if a property with the same title, location, and owner exists.
        
        Args:
            title (str): The title of the property.
            location (str): The location of the property.
            owner_id (UUID): The owner ID of the property.
            
        Returns:
            Property: The existing property if its found, else None
        
        """
        async with self.db:
            async with self.db.session as session:
                result = await session.execute(
                    select(Property).where(
                        #Case insensitive comparison for title and location
                        func.lower(Property.title) == func.lower(title),
                        func.lower(Property.location) == func.lower(location),
                        Property.owner_id == owner_id 
                    )
                )
                # Return the first matching property or None
                return result.scalar()


    async def update_property(
        self,
        id: UUID,
        title: str,
        description: str,
        price: float,
        size: float,
        status: str,
        location: str,
        neighborhood: str,
        city: str,
        country: str,
        legalStatus: str,
        images: list[str]
    ) -> Optional[Property]:
        """
        Update an existing property.
        
        args:
            id (UUID): The id of the property to be updated.
            title (str): The title of the property.
            description (str): The description of the property.
            price (float): The price of the property.
            size (float): The size of the property.
            status (str): The status of the property.
            location (str): The location of the property.
            neighborhood (str): The neighborhood of the property.
            city (str): The city of the property.
            country (str): The country of the property.
            legalStatus (str): The legal status of the property.
            images (list[str]): The images of the property.
            
        Returns:
            Property: The updated property
        """
        async with self.db:
            async with self.db.session as session:
                property_ = await session.get(Property, id)
                if property_ is None:
                    return None

                # Update fields explicitly
                property_.title = title
                property_.description = description
                property_.price = price
                property_.size = size
                property_.status = status
                property_.location = location
                property_.neighborhood = neighborhood
                property_.city = city
                property_.country = country
                property_.legalStatus = legalStatus
                property_.images = images

                await session.commit()
                await session.refresh(property_)

        return property_


    async def delete_property(self, id: UUID):
        """
        Delete a property.
        
        Args:
            id (UUID): The id of the property to be deleted.
            
        Returns:
            bool: True if the property was deleted, False otherwise
        """
        async with self.db:
            async with self.db.session as session:
                property_ = await session.get(Property, id)
                if property_ is not None:
                    await session.delete(property_)
                    await session.commit()
                    return True
                return False

    async def get_property(self, id: UUID):
        """
        Get a property by id.
        
        Args:
            id (UUID): The id of the property.
        
        Returns:
            Property: The property object if found, else None
        """
        async with self.db:
            async with self.db.session as session:
                return await session.get(Property, id)

    async def list_properties(self):
        """
        List all properties.
        
        Returns:
            list[Property]: A list of all properties
        """
        async with self.db:
            async with self.db.session as session:
                properties = await session.execute(select(Property))
                return properties.scalars().all()
