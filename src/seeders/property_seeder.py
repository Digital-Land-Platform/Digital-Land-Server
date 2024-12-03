import json
import random
from sqlalchemy.ext.asyncio import AsyncSession
from src.graphql.property.services import PropertyService
from src.models.enums.PropertyStatus import PropertyStatus
from src.graphql.property.types import PropertyInput
from src.graphql.image.types import ImageInput
from src.graphql.users.services import UserService
from src.graphql.location.service import LocationService
from src.graphql.amenity.services import AmenityService

class PropertySeeder:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.property_service = PropertyService(self.db.SessionLocal())
        self.user_service = UserService(self.db)
        self.location_service = LocationService(self.db)
        self.amenity_service = AmenityService(self.db.SessionLocal())

    async def seed_properties(self, properties_data: list):
        for property_data in properties_data:
            status = (
                PropertyStatus[property_data["status"]]
                if property_data["status"] in PropertyStatus.__members__
                else PropertyStatus.PENDING
            )
            
            image_inputs = [ImageInput(file=img.get("file"), url=img.get("url")) for img in property_data.get("images", [])]
            
            property_input = PropertyInput(
                title=property_data["title"],
                description=property_data["description"],
                price=property_data["price"],
                size=property_data["size"],
                status=status,
                location_id=property_data["location_id"],
                user_id=property_data["user_id"],
                neighborhood=property_data["neighborhood"],
                latitude=property_data["latitude"],
                longitude=property_data["longitude"],
                yearBuilt=property_data["yearBuilt"],
                legalStatus=property_data["legalStatus"],
                disclosure=property_data["disclosure"],
                energyRating=property_data["energyRating"],
                streetViewUrl=property_data["streetViewUrl"],
                futureDevelopmentPlans=property_data["futureDevelopmentPlans"],
                zoningInformation=property_data["zoningInformation"],
                amenity_ids=property_data["amenity_ids"],
                images=image_inputs
            )
            locations = await self.location_service.get_all_locations()
            users = await self.user_service.get_all_users()
            amenitys = await self.amenity_service.list_all_amenities()
            for key, value in property_input.items():
                if key == "user_id":
                    property_input[key] = random.choice([user.id for user in users])
                if key == "location_id":
                    property_input[key] = random.choice([location.id for location in locations])
                if key == "amenity_ids":
                    property_input[key] = [random.choices([amenity.id for amenity in amenitys])]

            existing_property = await self.property_service.get_existing_property(
                title=property_input.title,
                location_id=property_input.location_id
            )

            if existing_property:
                print(f"Property '{property_input.title}' already exists.")
                continue
            
            await self.property_service.create_property(
                property_input=property_input,
                user_id=property_data.get("user_id"),
                amenity_ids=property_input.amenity_ids,
                images=property_input.images,
                location_id=property_input.location_id,
            )
