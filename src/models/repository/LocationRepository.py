from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.models.Location import Location
from sqlalchemy import and_
from sqlalchemy.sql import func

class LocationRepository:

    def __init__(self, db: AsyncSession):
        """
        Initializes the location repository with the database session.
    
        Args:
            db (AsyncSession): The database session.
        """
        self.db = db
    
    
    async def get_location_by_id(self, location_id: str) -> Location:
        """
        Fetch a location by its ID.

        Args:
            location_id (int): The ID of the location to fetch.

        Returns:
            Location: The found location.
        """
        try:
            async with self.db:
                async with self.db.session as session:
                    statement = select(Location).where(Location.id == location_id)
                    result = await session.execute(statement)
                    location = result.scalar_one_or_none()
                    if not location:
                        raise Exception("Location not found")
                    return location
        except Exception as e:
            raise Exception(f"Failed to fetch location by ID: {e}")
    
    async def get_all_locations(self) -> list[Location]:
        """
        Fetch all locations.

        Returns:
            list[Location]: A list of all locations.
        """
        try:
            async with self.db:
                async with self.db.session as session:
                    statement = select(Location)
                    result = await session.execute(statement)
                    locations = result.scalars().all()
                    return locations
        except Exception as e:
            raise Exception(f"Failed to fetch all locations: {e}")
    async def get_locations_by_country_province_sector(self, country: str, province: str, sector: str) -> list[Location]:
        """
        Retrieve locations by province and country.
        """
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(Location).where(
                            and_(
                                func.trim(func.lower(Location.province)) == province.lower(),
                                func.trim(func.lower(Location.country)) == country.lower(),
                                func.trim(func.lower(Location.sector)) == sector.lower()
                            )
                        )
                    )
                    return result.scalars().all() 

        except Exception as e:
            raise Exception(f"Failed to fetch locations by province and country: {e}")
