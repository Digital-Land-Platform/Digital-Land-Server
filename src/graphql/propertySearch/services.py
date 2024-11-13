from typing import List
from src.graphql.property.types import PropertyType
from .types import PropertySearchInput
from src.models.repository.PropertySearchRepository import PropertySearchRepository
from sqlalchemy.ext.asyncio import AsyncSession

class PropertySearchService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = PropertySearchRepository(db)
        

    async def search_properties(self, search_input: PropertySearchInput) -> List[PropertyType]:
        """Search for properties based on the input filters
        Args:
            search_input (PropertySearchInput): The filters to apply
        Returns:
            List[PropertyType]: The properties that match the filters
        """
        try:
            properties = await self.repository.search_properties(search_input)
            return [PropertyType(
                id=property.id,
                title=property.title,
                description=property.description,
                price=property.price,
                size=property.size,
                status=property.status,
                neighborhood=property.neighborhood,
                location_id=property.location_id,
                latitude=property.latitude,
                longitude=property.longitude,
                images=property.images, 
                streetViewUrl=property.street_view_url,
                yearBuilt=property.year_built,
                legalStatus=property.legal_status,
                disclosure=property.disclosure,
                energyRating=property.energy_rating,
                futureDevelopmentPlans=property.future_development_plans,
                zoningInformation=property.zoning_information,
                amenities=property.amenities,  
                owner_id=property.user_id
            ) for property in properties]
        except Exception as e:
            print(f"An error occurred while searching for properties: {e}")
            return []
        
        
        
