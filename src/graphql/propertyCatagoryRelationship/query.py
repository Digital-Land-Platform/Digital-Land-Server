from typing import List
import strawberry
from .services import PropertyCatagoryRelationService
from .types import PropertyCatagoryRelationshipType
from config.database import db
from src.graphql.property.types import PropertyType
from uuid import UUID

catagory_relationship_service = PropertyCatagoryRelationService(db)

@strawberry.type
class PropertyCatagoryRelationshipQuery:

    @strawberry.field
    async def get_relation_by_catagory_id(self, catagory_id: str) -> PropertyCatagoryRelationshipType:
        try:
            catagory = await catagory_relationship_service.get_relation_by_catagory_id(catagory_id)
            return PropertyCatagoryRelationshipType.from_orm(catagory)
        except Exception as e:
            raise Exception(f"Error fetching catagory relationship: {e}")
    
    @strawberry.field
    async def get_relation_by_property_id(self, property_id: str) -> List[PropertyCatagoryRelationshipType]:
        try:
            catagories = await catagory_relationship_service.get_relation_by_property_id(property_id)
            return [PropertyCatagoryRelationshipType.from_orm(catagory) for catagory in catagories]
        except Exception as e:
            raise Exception(f"Error fetching catagory relationship: {e}")
    
    @strawberry.field
    async def get_properties_by_category_id(self, category_id: UUID) -> List[PropertyType]:
        try:
            # Fetch properties associated with the category ID
            properties = await catagory_relationship_service.get_properties_by_category_id(category_id)
            
            # Map the properties to PropertyType instances and return the list
            return [
                PropertyType(
                    id=str(property.id),
                    title=property.title,
                    description=property.description,
                    price=property.price,
                    size=property.size,
                    status=property.status,
                    neighborhood=property.neighborhood,
                    latitude=property.latitude,
                    longitude=property.longitude,
                    location_id=str(property.location_id) if property.location_id else None,
                    street_view_url=property.street_view_url,
                    year_built=property.year_built,
                    legal_status=property.legal_status,
                    disclosure=property.disclosure,
                    energy_rating=property.energy_rating,
                    future_development_plans=property.future_development_plans,
                    zoning_information=property.zoning_information,
                    images=property.images,
                    amenities=property.amenities,
                    owner_id=property.user_id,
                ) 
                for property in properties
            ]
        except Exception as e:
            raise Exception(f"Error fetching properties by category ID: {e}")