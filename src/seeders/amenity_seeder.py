import json
import os
import sys
from sqlalchemy.ext.asyncio import AsyncSession

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.models.Amenity import Amenity
from src.models.repository.AmenityRepository import AmenityRepository

class AmenitySeeder:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.amenity_repo = AmenityRepository(self.db)

    async def delete_all_amenities(self):
        await self.amenity_repo.delete_all_amenities()

    async def seed_amenities_from_json(self):
        try:
            await self.delete_all_amenities()  # Delete all amenities before seeding

            current_dir = os.path.dirname(__file__)
            file_path = os.path.join(current_dir, "files", "amenities.json")

            with open(file_path, "r") as file:
                amenities = json.load(file)

            for amenity in amenities:
                amenity_data = Amenity(**amenity)
                await self.amenity_repo.create_amenity(amenity_data)
        except Exception as e:
            print(f"Failed to seed amenities: {e}")
            raise e