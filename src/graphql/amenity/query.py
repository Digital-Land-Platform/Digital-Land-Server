import strawberry
from uuid import UUID
from typing import Optional, List
from .services import AmenityService
from .index import AmenitiesType
from src.startups.dbConn import db
from src.models.Amenities import Amenities
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.repository.AmenityRepository import AmenityRepository

service = AmenityService(db)

@strawberry.type
class AmenityQuery:
    @strawberry.field
    async def get_amenity(self, amenity_id: UUID) -> Optional[AmenitiesType]:
        """
        Retrieve a single amenity by ID.

        Args:
            amenity_id (UUID): The ID of the amenity to retrieve.

        Returns:
            Optional[AmenitiesType]: The amenity if found, None otherwise.
        """
        return await service.get_amenity_by_id(amenity_id)

    @strawberry.field
    async def list_amenities(self) -> List[AmenitiesType]:
        """
        Retrieve a list of all amenities.

        Returns:
            List[AmenitiesType]: List of all amenities.
        """
        return await service.list_all_amenities()