from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.repository.LocationRepository import LocationRepository
from src.models.Location import Location


class LocationService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.location_repo = LocationRepository(self.db)

    async def get_location_by_id(self, location_id: str) -> Optional[Location]:
        """
        Retrieve a single location by ID.

        Args:
            location_id (UUID): The ID of the location to retrieve.

        Returns:
            Optional[Location]: The location if found, None otherwise.
        """
        return await self.location_repo.get_location_by_id(location_id)

    