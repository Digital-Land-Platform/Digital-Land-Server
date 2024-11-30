from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.models.Location import Location


class LocationRepository:

    def __init__(self, db: AsyncSession):
        """
        Initializes the location repository with the database session.
    
        Args:
            db (AsyncSession): The database session.
        """
        self.db = db
    
    async def create_location(self, location: Location) -> Location:
        try:
            async with self.db as session:
                session.add(location)
                await session.commit()
                await session.refresh(location)
                return location
        except Exception as e:
            raise Exception(f"Failed to create location: {e}")
    
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
        
    async def delete_all_locations(self) -> bool:
        try:
            async with self.db as session:
                statement = select(Location)
                result = await session.execute(statement)
                locations = result.scalars().all()
                if not locations or len(locations) == 0:
                    return False
                for location in locations:
                    await session.delete(location)
                await session.commit()
                return True
        except Exception as e:
            # await self.db.rollback()
            raise Exception(f"Failed to delete all locations: {e}")