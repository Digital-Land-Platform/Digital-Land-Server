import os
import json
import asyncio
from config.database import DatabaseSession
from src.seeders.property_seeder import PropertySeeder


class Seeder:
    def __init__(self, db):
        self.db = db

    async def seed(self, json_file: str):
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"File not found: {json_file}")

        with open(json_file, "r") as file:
            properties_data = json.load(file)

        property_seeder = PropertySeeder(self.db)
        await property_seeder.seed_properties(properties_data)


async def main():
    # Resolve the JSON file path
    current_dir = os.path.dirname(__file__)
    json_file = os.path.join(current_dir, "property_data.json")

    # Seed the database
    async with DatabaseSession() as session:
        seeder = Seeder(session)
        await seeder.seed(json_file)


if __name__ == "__main__":
    asyncio.run(main())
