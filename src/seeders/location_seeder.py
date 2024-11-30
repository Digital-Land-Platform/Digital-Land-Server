import json
import os
import sys
from sqlalchemy.ext.asyncio import AsyncSession

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.models.Location import Location
from src.models.repository.LocationRepository import LocationRepository

class LocationSeeder:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.location_repo = LocationRepository(self.db)

    async def delete_all_locations(self):
        await self.location_repo.delete_all_locations()

    async def seed_locations_from_json(self):
        try:
            await self.delete_all_locations()  # Delete all locations before seeding

            current_dir = os.path.dirname(__file__)
            file_path = os.path.join(current_dir, "files", "locations.json")

            with open(file_path, "r") as file:
                locations = json.load(file)

            for location in locations:
                location_data = Location(**location)
                await self.location_repo.create_location(location_data)

        except Exception as e:
            print(f"Error seeding locations: {e}")
            raise e