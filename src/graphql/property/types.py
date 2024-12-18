from enum import Enum
import strawberry
from uuid import UUID
from typing import Optional, List
from sqlalchemy import DateTime, Text, Column, Integer, String, Float, ForeignKey
from datetime import datetime
from pydantic import BaseModel, Field, condecimal
from src.graphql.amenity.types import AmenitiesType
from src.graphql.location.types import LocationType 
from src.graphql.image.types import ImageTypes , ImageInput, ImageUpdateInput

@strawberry.enum
class PropertyStatusType(Enum):
    SELLING_CANCELLED = 'Selling Cancelled'
    LISTED = 'Listed'
    SOLD = 'SOLD'
    PENDING = 'PENDING'

@strawberry.input
class PropertyBaseInput:
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    size: Optional[float] = None
    status: Optional[PropertyStatusType] = None
    #location: Optional[str] = None
    neighborhood: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    images: Optional[List[str]] = None
    streetViewUrl: Optional[str] = None
    yearBuilt: Optional[int] = None
    legalStatus: Optional[str] = ""
    disclosure: Optional[str] = None
    energyRating: Optional[str] = None
    futureDevelopmentPlans: Optional[str] = None
    zoningInformation: Optional[str] = None
    #amenities: Optional[List[UUID]] = None
#The PropertyType for property data
  
@strawberry.type
class ImageType:
    url: str
     
@strawberry.type
class PropertyType:
    id: str | None
    title: str | None
    description: str | None
    price: float | None
    size: float | None
    status: str | None
    neighborhood: str | None
    location_id: str | None 
    latitude: Optional[float] | None
    longitude: Optional[float] | None
    images: List[ImageTypes] | None
    street_view_url: Optional[str] | None
    year_built: Optional[int] | None
    legal_status: str | None
    disclosure: Optional[str] | None
    energy_rating: Optional[str] | None
    future_development_plans: Optional[str] | None
    zoning_information: Optional[str] | None
    amenities: List[AmenitiesType] | None
    owner_id: UUID | None
    
# The PropertyInput for creating a new property
@strawberry.input
class PropertyInput(PropertyBaseInput):
    # Accept the user_id in input but map it to owner_id in logic
    user_id: UUID
    amenity_ids: Optional[List[UUID]] = None
    images: Optional[List[ImageInput]] = None
    location_id: Optional[UUID] = None
# The PropertyUpdateInput for updating an existing property
@strawberry.input
class PropertyUpdateInput(PropertyBaseInput):
    id: str
    amenity_ids: Optional[List[UUID]] = None
    images: Optional[List[ImageUpdateInput]] = None
    location_id: Optional[UUID] = None
    
