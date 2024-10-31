import strawberry
from uuid import UUID
from typing import Optional, List
from src.models.Amenities import Amenities


@strawberry.type
class AmenitiesType:
    title: str
    icon: str
    
@strawberry.input
class AmenityInput:
    title: str
    icon: str

@strawberry.input
class AmenityUpdateInput:
    amenity_id: UUID
    title: Optional[str] = None
    icon: Optional[str] = None