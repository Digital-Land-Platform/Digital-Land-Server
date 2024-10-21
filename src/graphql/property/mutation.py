import strawberry
from typing import Optional
from uuid import UUID
from .services import PropertyService  
from .index import OwnerType, OwnerInput, OwnerUpdateInput, PropertyInput, PropertyUpdateInput, PropertyType

property_service = PropertyService()


@strawberry.type
class PropertyMutation:
    
    @strawberry.mutation
    async def create_owner(
        self,
        input: OwnerInput
    ) -> OwnerType:
        owner = await property_service.create_owner(input.name, input.contact_info, input.address)
        return OwnerType(
            id=owner.id,
            name=owner.name,
            contact_info=owner.contact_info,
            address=owner.address
        )

    @strawberry.mutation
    async def update_owner(
        self, 
        input: OwnerUpdateInput
    ) -> OwnerType:
        owner = await property_service.update_owner(input.id, input.name, input.contact_info, input.address)
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
        input: PropertyInput
    ) -> PropertyType:
        property_ = await property_service.create_property(
            id=id,
            title=input.title,
            description=input.description,
            price=input.price,
            size=input.size,
            location=input.location,
            neighborhood=input.neighborhood,
            city=input.city,
            country=input.country,
            legalStatus=input.legalStatus,
            images=input.images,
            owner_id=input.owner_id,
            status=input.status
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
        input: PropertyUpdateInput
    ) -> PropertyType:
        property_ = await property_service.update_property(
            id=input.id,
            title=input.title,
            description=input.description,
            price=input.price,
            size=input.size,
            status=input.status,
            location=input.location,
            neighborhood=input.neighborhood,
            city=input.city,
            country=input.country,
            legalStatus=input.legalStatus,
            images=input.images
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
