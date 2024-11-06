import strawberry
from .types import LocationType
from .service import LocationService
from config.database import db

location_service = LocationService(db)

@strawberry.type
class LocationQuery:

    @strawberry.field
    async def get_location(self, location_id: str) -> LocationType:
        location = await location_service.get_location_by_id(location_id)
        return LocationType.from_model(location) if location else None