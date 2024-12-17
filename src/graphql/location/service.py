from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.middleware.ErrorHundlers.CustomErrorHandler import InternalServerErrorException
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
        try:
            return await self.location_repo.get_location_by_id(location_id)
        except Exception as e:
            raise InternalServerErrorException()

    async def get_all_locations(self) -> list[Location]:
        """
        Retrieve all locations.

        Returns:
            list[Location]: A list of all locations.
        """
        try:
            return await self.location_repo.get_all_locations()
        except Exception as e:
            raise InternalServerErrorException()

    