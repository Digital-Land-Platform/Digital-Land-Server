import json
import os
import sys
import random
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.models.User import User
from src.models.UserProfile import UserProfile
from src.models.enums.UserRole import UserRole
from src.models.enums.AccountStatus import AccountStatus
from src.models.repository.userRepository import UserRepository
from src.models.repository.UserProfileRepository import UserProfileRepository
from src.middleware.UserProfileValidator import UserProfileValidator
from src.models.repository.LocationRepository import LocationRepository

class UserSeeder:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(self.db)
        self.profile_repo = UserProfileRepository(self.db)
        self.location_repo = LocationRepository(self.db)

    async def delete_all_users(self):
        await self.user_repo.delete_all_users()


    async def seed_users_from_json(self):
        await self.delete_all_users()  # Delete all users before seeding

        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "files", "users.json")

        with open(file_path, "r") as file:
            users = json.load(file)

        locations = await self.location_repo.get_all_locations()
        location_list = [value.id for value in locations]

        if not location_list or len(location_list) == 0:
            print(f"Location list is empty {location_list}")
            raise Exception("No locations found in the database. Please add locations before seeding users.")
    
        for user in users:
            profile = user.pop("profile")
            user["role"] = UserRole[user["role"].upper()]
            user["account_status"] = AccountStatus[user["account_status"].upper()]
            user["last_login"] = datetime.fromisoformat(user["last_login"]) if user["last_login"] else None
            user_data = await self.user_repo.create_user(User(**user))
            profile["user_id"] = user_data.id
            profile["date_of_birth"] = UserProfileValidator.change_str_date(profile["date_of_birth"])
            profile["location_id"] = random.choice(location_list)
            profile_data = await self.profile_repo.create_user_profile(UserProfile(**profile))