import strawberry
from typing import List
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from src.graphql.property.types import PropertyType
from .types import PropertySearchInput
from .services import PropertySearchService
from src.startups.dbConn import db

service = PropertySearchService(db)
@strawberry.type
class PropertySearchQuery:
    def __init__(self, service: PropertySearchService):
        self.service = service

    @strawberry.field
    @ExceptionHandler.handle_exceptions
    async def search_properties(
        self,
        filters: PropertySearchInput,
    ) -> List[PropertyType]:
        """
        Search for properties based on the input filters
        Args:
            filters (PropertySearchInput): The filters to apply
        Returns:
            List[PropertyType]: The properties that match the filters
        """
        return await service.search_properties(filters)