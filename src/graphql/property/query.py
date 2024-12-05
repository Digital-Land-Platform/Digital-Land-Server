import strawberry
from uuid import UUID
from typing import Optional, List
from .services import PropertyService  
from .mutation import PropertyType 
from .types import AmenitiesType 
from src.startups.dbConn import db  
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.Property import Property
from src.models.repository.propertyRepository import PropertyRepository

service = PropertyService(db)

@strawberry.type
class PropertyQuery:

    @strawberry.field
    async def get_property(self, id: Optional[UUID]) -> Optional[PropertyType]:
        """
        Retrieve a property by its ID.
        
        Args:
            id (UUID): The ID of the property to retrieve.
            
        Returns:
            Optional[PropertyType]: The property object if found, None otherwise.
        """
        
        return await service.get_property(id)

    @strawberry.field
    async def list_properties(self) -> List[PropertyType]:
        """
        List all properties.
        
        Returns:
            List[PropertyType]: A list of all properties.
        """
        return await service.list_properties()
    