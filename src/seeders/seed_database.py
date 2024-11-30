# #!/user/bin/python3  
import os
import json
import asyncio
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.seeders.property_seeder import PropertySeeder
from config.database import db
from src.seeders.location_seeder import LocationSeeder
from src.seeders.organization_seeder import OrganizationSeeder
from src.seeders.user_seeder import UserSeeder
from src.seeders.amenity_seeder import AmenitySeeder
from main import app


class Seeder:
    def __init__(self, db):
        self.db = db

    async def seed(self):
        current_dir = os.path.dirname(__file__)
        json_file = os.path.join(current_dir, "property_data.json")
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"File not found: {json_file}")

        with open(json_file, "r") as file:
            properties_data = json.load(file)

        await LocationSeeder(self.db).seed_locations_from_json()
        await UserSeeder(self.db).seed_users_from_json()
        await OrganizationSeeder(self.db).seed_organizations_from_json()
        await AmenitySeeder(self.db).seed_amenities_from_json()
        await PropertySeeder(self.db).seed_properties(properties_data)
        
        

if __name__ == "__main__":
    import asyncio
    
    async def main():
        try:
            await db.create_all()
            await Seeder(db).seed()
        except Exception as e:
            print(e)
            await db.close()
        finally:
            await db.close()
            print("Database connection closed.")
    
    asyncio.run(main())