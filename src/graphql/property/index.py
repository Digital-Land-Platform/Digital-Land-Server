import strawberry
from uuid import UUID
from typing import Optional, List
from sqlalchemy import DateTime, Text, Column, Integer, String, Float, ForeignKey
from datetime import datetime
from pydantic import BaseModel, Field, condecimal
from src.graphql.amenity.index import AmenitiesType
    
@strawberry.input
class PropertyBaseInput:
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    size: Optional[float] = None
    status: Optional[str] = None
    location: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    images: Optional[List[str]] = None
    virtualTourUrl: Optional[str] = None
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
    id: str
    title: str
    description: str
    price: float
    size: float
    status: str
    location: str
    neighborhood: str
    city: str
    country: str
    latitude: Optional[float]
    longitude: Optional[float]
    images: List[ImageType]
    virtualTourUrl: Optional[str]
    streetViewUrl: Optional[str]
    yearBuilt: Optional[int]
    legalStatus: str
    disclosure: Optional[str]
    energyRating: Optional[str]
    futureDevelopmentPlans: Optional[str]
    zoningInformation: Optional[str]
    amenities: List[AmenitiesType]
    owner_id: UUID  
    
# The PropertyInput for creating a new property
@strawberry.input
class PropertyInput(PropertyBaseInput):
    # Accept the user_id in input but map it to owner_id in logic
    user_id: UUID
    amenity_ids: Optional[List[UUID]] = None

# The PropertyUpdateInput for updating an existing property
@strawberry.input
class PropertyUpdateInput(PropertyBaseInput):
    id: UUID
    amenity_ids: Optional[List[UUID]] = None

    
