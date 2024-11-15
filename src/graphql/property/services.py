# src/graphql/property/services.py
from typing import Optional, List
from src.models.repository.propertyRepository import PropertyRepository
from src.models.repository.AmenityRepository import AmenityRepository
from src.models.repository.ImageRepository import ImageRepository
from src.models.repository.LocationRepository import LocationRepository
from uuid import UUID
from src.models.Property import Property
from src.models.Location import Location  
from sqlalchemy.ext.asyncio import AsyncSession
from .types import PropertyInput, PropertyUpdateInput, PropertyType
from src.graphql.amenity.types import AmenitiesType, AmenityUpdateInput
from src.graphql.image.types import ImageTypes, ImageInput, ImageUpdateInput
from .types import PropertyStatusType
from config.database import db as main_db
from src.graphql.image.services import ImageService 
from src.models.Amenity import Amenity as Amenities
from src.middleware.AuthManagment import AuthManagement
from strawberry.file_uploads import Upload
from src.models.enums.PropertyStatus import PropertyStatus



class PropertyService:
    def __init__(self, db: AsyncSession):
        """
        initializes the property service with the database session
        
        Args:
            db (AsyncSession): the database session
        """
        self.db = db
        self.repository = PropertyRepository(db)    
        self.amenity_repository = AmenityRepository(db)
        self.location_repository = LocationRepository(main_db)
        self.image_repository = ImageRepository(db)
        self.image_service = ImageService(db)
        

    async def create_property(
        self,
        property_input: PropertyInput,
        user_id: UUID,
        amenity_ids: Optional[List[UUID]] = None,
        images: Optional[List[ImageInput]] = None,
        location_id: Optional[UUID] = None
    ) -> Property:
        """
        creates a new property in the database
        
        Args:
            property_input (PropertyInput): the input data for the property
            user_id (UUID): the id of the user creating the property
            
        Returns:
            Property: the created property
        """
        location_id = await self.location_repository.get_location_by_id(location_id)
        if not location_id:
            raise ValueError("Location not found for the given location_id")
        
        status = PropertyStatus.PENDING
        if property_input.status.value == PropertyStatus.LISTED.value:
            status = PropertyStatus.LISTED
        elif property_input.status.value == PropertyStatus.SELLING_CANCELLED.value:
            status = PropertyStatus.SELLING_CANCELLED
        elif property_input.status.value == PropertyStatus.SOLD.value:
            status = PropertyStatus.SOLD
            
        new_property = Property(
            title=property_input.title,
            user_id=property_input.user_id,  
            description=property_input.description,
            price=property_input.price,
            size=property_input.size,
            status= status,  
            location_id=property_input.location_id,
            neighborhood=str(property_input.neighborhood),  # String column
    latitude=str(property_input.latitude),  # String column
    longitude=str(property_input.longitude),
            year_built=property_input.yearBuilt,
            legal_status=str(property_input.legalStatus),  # String column
    disclosure=str(property_input.disclosure),  # String column
    energy_rating=str(property_input.energyRating),  # String column
    street_view_url=str(property_input.streetViewUrl),
            future_development_plans=property_input.futureDevelopmentPlans,
            zoning_information=property_input.zoningInformation
        )
        new_property = await self.repository.create_property(new_property)
        
        
        if property_input.images:
            for image_input in property_input.images:
                if image_input.file:
                    image_input = ImageInput(file=image_input.file)
                    await self.image_service.create_image(image_input, new_property.id)
                    
        if property_input.amenity_ids:
            amenities = await self.amenity_repository.get_amenities_by_ids(property_input.amenity_ids)
            new_property.amenities = amenities
         
        else:
            new_property.amenities = []

        return await self.repository.create_property(new_property)
        
    async def get_existing_property(self, title: str, location_id: str):
        """
        gets an existing property from the database
        
        Args:
            title (str): the title of the property
            location_id (str): the location_id of the property
            owner_id (UUID): the id of the owner of the property
            
        Returns:
            Property: the existing property
        """
        return await self.repository.get_existing_property(title, location_id)

    async def update_property(
        self,
        property_update_input: PropertyUpdateInput,
        amenity_ids: Optional[List[UUID]] = None,
        images: Optional[List[ImageUpdateInput]] = None,
        location_id: Optional[UUID] = None,
    ) -> Optional[Property]:
        """
        updates an existing property in the database
        
        Args:
            property_update_input (PropertyUpdateInput): the input data for the property update
            
        Returns:
            Optional[Property]: the updated property
        """
        
        id = property_update_input.id
        property_ = await self.repository.get_property(id=id)
        
        if not property_:
            return None
        
        if location_id:
            location_id = await self.location_repository.get_location_by_id(location_id)
            if location_id:
                property_.location_id = location_id.id
            else:
                raise ValueError("Location not found for the given location_id")
        status = PropertyStatus.PENDING
        if property_update_input.status.value == PropertyStatus.LISTED.value:
            status = PropertyStatus.LISTED
        elif property_update_input.status.value == PropertyStatus.SELLING_CANCELLED.value:
            status = PropertyStatus.SELLING_CANCELLED
        elif property_update_input.status.value == PropertyStatus.SOLD.value:
            status = PropertyStatus.SOLD        

        if property_update_input.title is not None:
            property_.title = str(property_update_input.title)
        if property_update_input.description is not None:
            property_.description = str(property_update_input.description)
        if property_update_input.price is not None:
            property_.price = property_update_input.price
        if property_update_input.size is not None:
            property_.size = property_update_input.size
        if property_update_input.status is not None:
            property_.status = status
        if property_update_input.location_id is not None:
            property_.location_id = property_update_input.location_id
        if property_update_input.neighborhood is not None:
            property_.neighborhood = str(property_update_input.neighborhood)
        if property_update_input.latitude is not None:
            property_.latitude = str(property_update_input.latitude)
        if property_update_input.longitude is not None:
            property_.longitude = str(property_update_input.longitude)
        if property_update_input.streetViewUrl is not None:
            property_.street_view_url = str(property_update_input.streetViewUrl)
        if property_update_input.yearBuilt is not None:
            property_.year_built = property_update_input.yearBuilt
        if property_update_input.legalStatus is not None:
            property_.legal_status = str(property_update_input.legalStatus)
        if property_update_input.disclosure is not None:
            property_.disclosure = str(property_update_input.disclosure)
        if property_update_input.energyRating is not None:
            property_.energy_rating = str(property_update_input.energyRating)
        if property_update_input.futureDevelopmentPlans is not None:
            property_.future_development_plans = property_update_input.futureDevelopmentPlans
        if property_update_input.zoningInformation is not None:
            property_.zoning_information = property_update_input.zoningInformation



        # Update images and amenities if provided
        if property_update_input.images is not None:
            for image_update_input in property_update_input.images:
                if image_update_input.image_id and (image_update_input.file or image_update_input.url):
                    print(f"Updating image with ID: {image_update_input.image_id}")
                    await self.image_service.update_image(image_update_input)  
                              
        if property_update_input.amenity_ids is not None:
            # Clear existing amenities
            existing_amenities = {amenity.id for amenity in property_.amenities}
            # Fetch new amenities
            for amenity_id in property_update_input.amenity_ids:
                if amenity_id not in existing_amenities:
                # Fetch the amenity to add
                    new_amenity = await self.amenity_repository.get_amenity_by_id(amenity_id)
                    if new_amenity:
                        property_.amenities.append(new_amenity)
                        
                
        await self.repository.update_property(property_)
        return property_
    
    
    async def delete_property(self, id):
        """
        deletes a property from the database
        
        Args:
            id (UUID): the id of the property to delete
            
        Returns:
            bool: True if the property was deleted, False otherwise
        """
        return await self.repository.delete_property(id)

    async def get_property(self, id: UUID) -> Optional[Property]:
        """
        retrieves a property from the database
        
        Args:
            id (UUID): the id of the property to retrieve
            
        Returns:
        
            Optional[Property]: the property if found, None otherwise
        """
        return await self.repository.get_property(id)

    async def list_properties(self) -> List[Property]:
        """
        retrieves a list of all properties from the database
        
        Returns:
            List[Property]: the list of properties
        """
        return await self.repository.list_properties() 
    
    async def change_user_status(self, property_id: str, property_data: dict) -> Property:
        try:
            property = await self.repository.get_property(property_id)
            for key, value in property_data.items():
                if value and hasattr(property, key):
                    setattr(property, key, value)
            await self.repository.update_property(property)
            return property
        except Exception as e:  
            raise Exception(f"Error updating property: {e}")