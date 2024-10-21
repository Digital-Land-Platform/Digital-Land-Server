import strawberry
from uuid import UUID
from typing import Optional

# Define OwnerType for owner data
@strawberry.type
class OwnerType:
    id: UUID
    name: str
    contact_info: str
    address: Optional[str]

@strawberry.input
class OwnerInput:
    name: str
    contact_info: str
    address: Optional[str] = None
    
@strawberry.input
class OwnerUpdateInput:
    id: UUID
    name: Optional[str] = None
    contact_info: Optional[str] = None
    address: Optional[str] = None

# Define PropertyType for property data
@strawberry.type
class PropertyType:
    id: UUID
    title: str
    description: str
    price: float
    size: float
    location: str
    neighborhood: str
    city: str
    country: str
    status: str
    images: str
    legalStatus: str
    owner_id: UUID

# Define PropertyInput for creating a new property
@strawberry.input
class PropertyInput:
    title: str
    description: str
    price: float
    size: float
    location: str
    neighborhood: str
    city: str
    country: str
    legalStatus: str
    images: str
    owner_id: UUID
    status: Optional[str] = "available"

# Define PropertyUpdateInput for updating an existing property
@strawberry.input
class PropertyUpdateInput:
    id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    size: Optional[float] = None
    status: Optional[str] = None
    location: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    legalStatus: Optional[str] = None
    images: Optional[str] = None
