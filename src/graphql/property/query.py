# src/graphql/property/query.py
import strawberry
from uuid import UUID
from typing import Optional, List
from .services import PropertyService  # Assuming service handles business logic
from .mutation import PropertyType  # Ensure these are imported

@strawberry.type
class PropertyQuery:
    @strawberry.field
    async def get_property(self, id: UUID) -> Optional[PropertyType]:
        """
        Retrirve a property by its ID.
        
        Args:
            id (UUID): The ID of the property to retrieve.
            
        Returns:
            Optional[PropertyType]: The property object if found, None otherwise.
        """
        service = PropertyService()
        return await service.get_property(id)

    @strawberry.field
    async def list_properties(self) -> List[PropertyType]:
        """
        List all properties.
        
        Returns:
            List[PropertyType]: A list of all properties.
        """
        service = PropertyService()
        return await service.list_properties()
