# src/graphql/property/services.py
from typing import Optional, List
from src.models.repository.propertyRepository import PropertyRepository
from src.models.repository.AmenityRepository import AmenityRepository
from uuid import UUID
from src.models.Property import Property  
from sqlalchemy.ext.asyncio import AsyncSession
from .index import PropertyInput, PropertyUpdateInput, PropertyType
from src.graphql.amenity.index import AmenitiesType, AmenityUpdateInput
from config.database import db
from src.models.Image import Image
from src.models.Amenities import Amenities
from src.middleware.AuthManagment import AuthManagement


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

    async def create_property(
        self,
        property_input: PropertyInput,
        user_id: UUID,
        amenity_ids: Optional[List[UUID]] = None
    ) -> Property:
        """
        creates a new property in the database
        
        Args:
            property_input (PropertyInput): the input data for the property
            user_id (UUID): the id of the user creating the property
            
        Returns:
            Property: the created property
        """

        
        new_property = Property(
            title=property_input.title,
            description=property_input.description,
            price=property_input.price,
            size=property_input.size,
            status=property_input.status or "available",  # Default value if not provided
            location=property_input.location,
            neighborhood=property_input.neighborhood,
            city=property_input.city,
            country=property_input.country,
            latitude=property_input.latitude,
            longitude=property_input.longitude,
            virtualTourUrl=property_input.virtualTourUrl,
            streetViewUrl=property_input.streetViewUrl,
            yearBuilt=property_input.yearBuilt,
            legalStatus=property_input.legalStatus,
            disclosure=property_input.disclosure,
            energyRating=property_input.energyRating,
            futureDevelopmentPlans=property_input.futureDevelopmentPlans,
            zoningInformation=property_input.zoningInformation,
            owner_id=property_input.user_id  # Map user_id to owner_id
        )
        
        if property_input.images:
            new_property.images = [Image(url=url) for url in property_input.images]

        if property_input.amenity_ids:
            amenities = await self.amenity_repository.get_amenities_by_ids(property_input.amenity_ids)
            new_property.amenities = amenities
         
        else:
            new_property.amenities = []

        return await self.repository.create_property(new_property)
        
    async def get_existing_property(self, title: str, location: str, owner_id: UUID):
        """
        gets an existing property from the database
        
        Args:
            title (str): the title of the property
            location (str): the location of the property
            owner_id (UUID): the id of the owner of the property
            
        Returns:
            Property: the existing property
        """
        return await self.repository.get_existing_property(title, location, owner_id)

    async def update_property(
        self,
        property_update_input: PropertyUpdateInput,
        amenity_ids: Optional[List[UUID]] = None
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
        
        if property_update_input.title is not None:
            property_.title = property_update_input.title
        if property_update_input.description is not None:
            property_.description = property_update_input.description
        if property_update_input.price is not None:
            property_.price = property_update_input.price
        if property_update_input.size is not None:
            property_.size = property_update_input.size
        if property_update_input.status is not None:
            property_.status = property_update_input.status
        if property_update_input.location is not None:
            property_.location = property_update_input.location
        if property_update_input.neighborhood is not None:
            property_.neighborhood = property_update_input.neighborhood
        if property_update_input.city is not None:
            property_.city = property_update_input.city
        if property_update_input.country is not None:
            property_.country = property_update_input.country
        if property_update_input.latitude is not None:
            property_.latitude = property_update_input.latitude
        if property_update_input.longitude is not None:
            property_.longitude = property_update_input.longitude
        if property_update_input.virtualTourUrl is not None:
            property_.virtualTourUrl = property_update_input.virtualTourUrl
        if property_update_input.streetViewUrl is not None:
            property_.streetViewUrl = property_update_input.streetViewUrl
        if property_update_input.yearBuilt is not None:
            property_.yearBuilt = property_update_input.yearBuilt
        if property_update_input.legalStatus is not None:
            property_.legalStatus = property_update_input.legalStatus
        if property_update_input.disclosure is not None:
            property_.disclosure = property_update_input.disclosure
        if property_update_input.energyRating is not None:
            property_.energyRating = property_update_input.energyRating
        if property_update_input.futureDevelopmentPlans is not None:
            property_.futureDevelopmentPlans = property_update_input.futureDevelopmentPlans
        if property_update_input.zoningInformation is not None:
            property_.zoningInformation = property_update_input.zoningInformation


        # Update images and amenities if provided
        if property_update_input.images is not None:
            for url in property_update_input.images:
                image = Image(url=url, property=property_)
                self.db.add(image)
                                
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
    
    