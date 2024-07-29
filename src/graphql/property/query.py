# src/graphql/property/query.py

import strawberry
from uuid import UUID
from typing import Optional, List
from .services import PropertyService  # Assuming service handles business logic
from .mutation import OwnerType, PropertyType  # Ensure these are imported

@strawberry.type
class PropertyQuery:
    @strawberry.field
    async def get_owner(self, id: UUID) -> Optional[OwnerType]:  # Specify return type
        service = PropertyService()
        return await service.get_owner(id)

    @strawberry.field
    async def get_property(self, id: UUID) -> Optional[PropertyType]:  # Specify return type
        service = PropertyService()
        return await service.get_property(id)

    @strawberry.field
    async def list_owners(self) -> List[OwnerType]:  # Specify return type
        service = PropertyService()
        return await service.list_owners()

    @strawberry.field
    async def list_properties(self) -> List[PropertyType]:  # Specify return type
        service = PropertyService()
        return await service.list_properties()
