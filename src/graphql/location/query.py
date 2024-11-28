import strawberry
from .types import LocationType
from .service import LocationService
from config.database import db

location_service = LocationService(db)

@strawberry.type
class LocationQuery:

    @strawberry.field
    async def get_location(self, location_id: str) -> LocationType:
        try:
            location = await location_service.get_location_by_id(location_id)
            return LocationType.from_model(location) if location else None
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to get Location: {e}")
    
    @strawberry.field
    async def get_locations(self) -> list[LocationType]:
        try:
            locations = await location_service.get_all_locations()
            return [LocationType.from_model(location) for location in locations]
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to get Locations: {e}")
    @strawberry.field
    async def get_locations_by_country_province_sector(
        self, country: str, province: str, sector: str
    ) -> list[LocationType]:
        try:
            locations = await location_service.get_locations_by_country_province_sector(country, province, sector)
            return [LocationType.from_model(location) for location in locations]
        except Exception as e:
            raise strawberry.exceptions.GraphQLError(f"Failed to get Locations: {e}")