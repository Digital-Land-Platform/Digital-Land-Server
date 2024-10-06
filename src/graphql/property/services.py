# src/graphql/property/services.py
from typing import Optional
from src.models.repository.propertyRepository import PropertyRepository
from uuid import UUID
from src.models.Property import Property  
from sqlalchemy.ext.asyncio import AsyncSession

class PropertyService:
    def __init__(self, db: AsyncSession):
        """
        initializes the property service with the database session
        
        Args:
            db (AsyncSession): the database session
        """
        self.db = db
        self.repository = PropertyRepository()

    async def create_property(
        self,
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
        images: str,
        owner_id: UUID
    ):
        """
        creates a new property in the database
        
        Args:
            title (str): the title of the property
            description (str): the description of the property
            price (float): the price of the property
            size (float): the size of the property
            status (str): the status of the property
            location (str): the location of the property
            neighborhood (str): the neighborhood of the property
            city (str): the city of the property
            country (str): the country of the property
            legalStatus (str): the legal status of the property
            images (str): the images of the property
            owner_id (UUID): the id of the owner of the property
            
        Returns:
            Property: the created property
        """
        return await self.repository.create_property(
            title=title,
            description=description,
            price=price,
            size=size,
            status=status,
            location=location,
            neighborhood=neighborhood,
            city=city,
            country=country,
            legalStatus=legalStatus,
            images=images,
            owner_id=owner_id
        )
        
    async def get_existing_property(self, title: str, location: str, owner_id: UUID):
        """
        gets an existing property from the database
        
        Args:
            title (str): the title of the property
            location (str): the location of the property
            owner_id (UUID): the id of the owner of the property
            
        Returns:
            Property: the existing property
        """
        return await self.repository.get_existing_property(title, location, owner_id)

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
        images: str
    ) -> Optional[Property]:
        """
        updates an existing property in the database
        
        Args:
            id (UUID): the id of the property
            title (str): the title of the property
            description (str): the description of the property
            price (float): the price of the property
            size (float): the size of the property
            status (str): the status of the property
            location (str): the location of the property
            neighborhood (str): the neighborhood of the property
            city (str): the city of the property
            country (str): the country of the property
            legalStatus (str): the legal status of the property
            images (str): the images of the property
            
            Returns:
                Optional[Property]: the updated property
            """
        return await self.repository.update_property(
            id=id,
            title=title,
            description=description,
            price=price,
            size=size,
            status=status,
            location=location,
            neighborhood=neighborhood,
            city=city,
            country=country,
            legalStatus=legalStatus,
            images=images
        )

    async def delete_property(self, id):
        return await self.repository.delete_property(id)

    async def get_property(self, id):
        return await self.repository.get_property(id)

    async def list_properties(self):
        return await self.repository.list_properties()
