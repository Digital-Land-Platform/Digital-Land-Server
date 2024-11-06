from typing import List
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.Property import Property
from src.graphql.propertySearch.types import PropertySearchInput
from src.models.Location import Location

class PropertySearchRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search_properties(self, search_input: PropertySearchInput) -> List[Property]:
        """Search for properties based on the input filters
        Args:
            search_input (PropertySearchInput): The filters to apply
        Returns:
            List[Property]: The properties that match the filters
        """
        # Start with a base query
        query = select(Property).join(Location, Property.location_id == Location.id)
        
        
        # Apply filters conditionally based on input
        filters = []
        
        if search_input.location:
            filters.append(func.lower(Location.province).like(f"%{search_input.location.lower()}%"))
        
        if search_input.min_price is not None:
            filters.append(Property.price >= search_input.min_price)
        
        if search_input.max_price is not None:
            filters.append(Property.price <= search_input.max_price)
        
        if search_input.min_size is not None:
            filters.append(Property.size >= search_input.min_size)
        
        if search_input.max_size is not None:
            filters.append(Property.size <= search_input.max_size)
        
        if search_input.status:
            filters.append(Property.status == search_input.status.value)

        # Combine all filters with AND and apply them to the query
        if filters:
            query = query.where(and_(*filters))

        # Apply pagination
        query = query.offset((search_input.page - 1) * search_input.limit).limit(search_input.limit)

        
        async with self.db as session:
            result = await session.execute(query)
            properties = result.scalars().unique()

        return properties     