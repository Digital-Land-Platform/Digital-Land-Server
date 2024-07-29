import strawberry
from typing import Optional
from uuid import UUID
from .services import PropertyService  # Assuming service handles business logic

property_service = PropertyService()

@strawberry.type
class OwnerType:
    id: UUID
    name: str
    contact_info: str
    address: Optional[str]

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

@strawberry.type
class PropertyMutation:
    
    @strawberry.mutation
    async def create_owner(
        self,
        name: str, 
        contact_info: str,
        address: Optional[str] = None
    ) -> OwnerType:
        owner = await property_service.create_owner(name, contact_info, address)
        return OwnerType(
            id=owner.id,
            name=owner.name,
            contact_info=owner.contact_info,
            address=owner.address
        )

    @strawberry.mutation
    async def update_owner(
        self,
        id: UUID, 
        name: Optional[str] = None,
        contact_info: Optional[str] = None,
        address: Optional[str] = None
    ) -> OwnerType:
        owner = await property_service.update_owner(id, name, contact_info, address)
        return OwnerType(
            id=owner.id,
            name=owner.name,
            contact_info=owner.contact_info,
            address=owner.address
        )

    @strawberry.mutation
    async def delete_owner(self, id: UUID) -> bool:
        result = await property_service.delete_owner(id)
        return result

    @strawberry.mutation
    async def create_property(
        self, 
        title: str, 
        description: str, 
        price: float, 
        size: float,
        location: str, 
        neighborhood: str,
        city: str,
        country: str, 
        legalStatus: str,
        images: str,
        owner_id: UUID,
        status: Optional[str] = "available"
    ) -> PropertyType:
        property_ = await property_service.create_property(
            id=id,
            title=title,
            description=description,
            price=price,
            size=size,
            location=location,
            neighborhood=neighborhood,
            city=city,
            country=country,
            legalStatus=legalStatus,
            images=images,
            owner_id=owner_id,  
            status=status 
        )
        return PropertyType(
            id=property_.id,
            title=property_.title,
            description=property_.description,
            price=property_.price,
            size=property_.size,
            location=property_.location,
            neighborhood=property_.neighborhood,
            city=property_.city,
            country=property_.country,
            status=property_.status,
            images=property_.images,
            legalStatus=property_.legalStatus,
            owner_id=property_.owner_id
        )

    @strawberry.mutation
    async def update_property(
        self,
        id: UUID,
        title: str,
        description: str,
        price: float,
        size: float,
        status: str,
        location: str,
        neighborhood: str,
        city: str,
        country: str,
        legalStatus: str,
        images: str
    ) -> PropertyType:
        property_ = await property_service.update_property(
            id=id,
            title=title,
            description=description,
            price=price,
            size=size,
            status=status,
            location=location,
            neighborhood=neighborhood,
            city=city,
            country=country,
            legalStatus=legalStatus,
            images=images
        )
        
        if property_ is None:
            raise Exception("Property not found")
        
        return PropertyType(
            id=property_.id,
            title=property_.title,
            description=property_.description,
            price=property_.price,
            size=property_.size,
            location=property_.location,
            neighborhood=property_.neighborhood,
            city=property_.city,
            country=property_.country,
            status=property_.status,
            images=property_.images,
            legalStatus=property_.legalStatus,
            owner_id=property_.owner_id
        )

    @strawberry.mutation
    async def delete_property(self, id: UUID) -> bool:
        result = await property_service.delete_property(id)
        return result
