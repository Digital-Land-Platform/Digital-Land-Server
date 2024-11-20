import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from config.database import db
from src.seeders.organization_seeder import OrganizationSeeder
from src.seeders.user_seeder import UserSeeder
from main import app


class Seeder:
    def __init__(self, db):
        self.db = db

    async def seed(self):
        await OrganizationSeeder(self.db).seed_organizations_from_json()
        await UserSeeder(self.db).seed_users_from_json()

if __name__ == "__main__":
    import asyncio
    
    async def main():
        await db.create_all()
        await Seeder(db).seed()
        await db.close()
    
    asyncio.run(main())