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
        self.session = self.db.SessionLocal()
        self.property_service = PropertyService(self.session)
        self.user_service = UserService(self.db)
        self.location_service = LocationService(self.db)
        self.amenity_service = AmenityService(self.session)

    async def seed_properties(self, properties_data: list):
        try:
            for property_data in properties_data:
                status = (
                    PropertyStatus[property_data["status"]]
                    if property_data["status"] in PropertyStatus.__members__
                    else PropertyStatus.PENDING
                )
                
            image_inputs = [ImageInput(file=img.get("file"), url=img.get("url")) for img in property_data.get("images", [])]
                
            
            locations = await self.location_service.get_all_locations()
            users = await self.user_service.get_all_users()
            amenities = await self.amenity_service.list_all_amenities()

            if not locations or len(locations) == 0:
                print("Properties can not be seeded because there are No locations found.")
                return
            
            if not users or len(users) == 0:
                print("Properties can not be seeded because there are No users found.")
                return
            
            if not amenities or len(amenities) == 0:
                print("Properties can not be seeded because there are No amenities found.")
                print(amenities)
                return

            for property_data in properties_data:
                property_data["location_id"] = random.choice([loc.id for loc in locations])
                property_data["user_id"] = random.choice([user.id for user in users])
                property_data["amenity_ids"] = [random.choice([amenity.id for amenity in amenities])]

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

                existing_property = await self.property_service.get_existing_property(
                        title=property_input.title,
                        location_id=property_input.location_id,
                    )

                if existing_property:
                    print(f"Property '{property_input.title}' already exists.")
                    continue

                await self.property_service.create_property(
                        property_input=property_input,
                        user_id=property_input.user_id,
                        location_id=property_input.location_id,
                        amenity_ids=property_input.amenity_ids,
                    )
        except Exception as e:
            print(f"Failed to seed properties: {e}")
            raise e
        finally:
            await self.session.close()
            print("Session closed.")