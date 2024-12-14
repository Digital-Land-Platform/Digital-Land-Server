import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from src.middleware.ErrorHundlers.CustomErrorHandler import InternalServerErrorException, BadRequestException
from .types import LocationType
from .service import LocationService
from config.database import db

location_service = LocationService(db)

@strawberry.type
class LocationQuery:

    @strawberry.field
    @ExceptionHandler.handle_exceptions
    async def get_location(self, location_id: str) -> LocationType:
        location = await location_service.get_location_by_id(location_id)
        if not location:
            raise BadRequestException("Location not found")
        return LocationType.from_model(location)
    
    @strawberry.field
    @ExceptionHandler.handle_exceptions
    async def get_locations(self) -> list[LocationType]:
        locations = await location_service.get_all_locations()
        return [LocationType.from_model(location) for location in locations]
    