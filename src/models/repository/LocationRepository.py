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