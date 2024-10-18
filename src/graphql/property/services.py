# src/graphql/property/services.py
from typing import Optional
from src.models.repository.propertyRepository import PropertyRepository
from uuid import UUID
from src.models.Property import Property  # Adjust the import according to your structure

class PropertyService:
    def __init__(self):
        self.repository = PropertyRepository()

    async def create_owner(self, name: str, contact_info: str, address: Optional[str] = None):
        return await self.repository.create_owner(name, contact_info, address)

    async def update_owner(self, id, name=None, contact_info=None, address=None):
        return await self.repository.update_owner(id, name, contact_info, address)

    async def delete_owner(self, id):
        return await self.repository.delete_owner(id)

    async def create_property(
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
        images: str,
        owner_id: UUID
    ):
        return await self.repository.create_property(
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
            images=images,
            owner_id=owner_id
        )

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
    ) -> Optional[Property]:
        return await self.repository.update_property(
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


    async def delete_property(self, id):
        return await self.repository.delete_property(id)

    async def get_owner(self, id):
        return await self.repository.get_owner(id)

    async def get_property(self, id):
        return await self.repository.get_property(id)

    async def list_owners(self):
        return await self.repository.list_owners()

    async def list_properties(self):
        return await self.repository.list_properties()
