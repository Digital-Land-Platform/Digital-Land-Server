import strawberry
from typing import Optional
from uuid import UUID
from src.models.repository.propertyRepository import PropertyRepository
from src.models.repository.AmenityRepository import AmenityRepository
from src.models.repository.LocationRepository import LocationRepository
from .services import PropertyService  
from .types import PropertyInput, PropertyUpdateInput, PropertyType, ImageType
from src.graphql.amenity.types import AmenityInput, AmenitiesType, AmenityUpdateInput
from src.middleware.AuthManagment import AuthManagement
from src.models.enums.UserRole import UserRole
from src.graphql.users.services import UserService
from config.database import db
from src.models.Amenity import Amenity as Amenities


# Initialize the services required for property mutations
property_service = PropertyService(db.SessionLocal())
auth_management = AuthManagement()
user_service = UserService(db.SessionLocal())

@strawberry.type
class PropertyMutation:
    @strawberry.mutation
    async def create_property(
        self, 
        property_input: PropertyInput,
        
    ) -> PropertyType:
        """
        Create a new property. Only users with the role of NOTARY or LAND_OWNER are allowed.
        
        Args:
            input (PropertyInput): The details of the property to be created.
            info: The GraphQL info context which contains request metadata.

        Returns:
            PropertyType: The created property object.
        """
        try:
            
            #check if property exists
            existing_property = await property_service.get_existing_property(
                title=property_input.title,
                location_id=property_input.location_id
            )
            
            if existing_property:
                raise Exception("A property with the same title and location already exists for this owner.")
             
            # Create the property
            property_ = await property_service.create_property(
                property_input=property_input,
                user_id=property_input.user_id,
                location_id=property_input.location_id
                
            )
            return PropertyType(
                id=property_.id,
                title=property_.title,
                description=property_.description,
                price=property_.price,
                size=property_.size,
                status=property_.status,
                location_id=property_input.location_id,
                neighborhood=property_.neighborhood,
                latitude=property_.latitude,
                longitude=property_.longitude,
                images=[ImageType(url=image.url) for image in property_.images],
                streetViewUrl=property_.street_view_url,
                amenities=[AmenitiesType(id=amenity.id, title=amenity.title, icon=amenity.icon) for amenity in property_.amenities],
                yearBuilt=property_.year_built,
                legalStatus=property_.legal_status,
                disclosure=property_.disclosure,
                energyRating=property_.energy_rating,
                futureDevelopmentPlans=property_.future_development_plans,
                zoningInformation=property_.zoning_information,
                owner_id=property_.user_id
            )
        except Exception as e:
            raise Exception(f"Failed to create property: {e}")

    @strawberry.mutation
    async def update_property(
        self,
        id: str,
        property_update_input: PropertyUpdateInput,
        info: strawberry.types.info   
    ) -> PropertyType:
        """
        Update an existing property.
        
        Args:
            input (PropertyUpdateInput): The details of the property to be updated.
            
        Returns:
            PropertyType: The updated property object.
        """
        
        try:
            updated_property = await property_service.update_property(
                #id=id,
                property_update_input=property_update_input
            )
        
            if updated_property is None:
                raise Exception("Failed to update property")

            # Return the updated property data
            return PropertyType(
                id=updated_property.id,
                title=updated_property.title,
                description=updated_property.description,
                price=updated_property.price,
                size=updated_property.size,
                status=updated_property.status,
                location_id=updated_property.location_id,
                neighborhood=updated_property.neighborhood,
                latitude=updated_property.latitude,
                longitude=updated_property.longitude,
                images=[ImageType(url=image.url) for image in updated_property.images],
                streetViewUrl=updated_property.street_view_url,
                amenities=[AmenitiesType(id=amenity.id, title=amenity.title, icon=amenity.icon) for amenity in updated_property.amenities],
                yearBuilt=updated_property.year_built,
                legalStatus=updated_property.legal_status,
                disclosure=updated_property.disclosure,
                energyRating=updated_property.energy_rating,
                futureDevelopmentPlans=updated_property.future_development_plans,
                zoningInformation=updated_property.zoning_information,
                owner_id=updated_property.user_id
            )
        except Exception as e:
            raise Exception(f"Failed to update property: {e}")
    
    @strawberry.mutation
    async def delete_property(self, id: UUID) -> bool:
        """
        Delete a property.
        
        Args:
            id (UUID): The id of the property to be deleted.
            
        Returns:
            bool: True if the property was deleted successfully, False otherwise.
        """
        result = await property_service.delete_property(id)
        return result
    