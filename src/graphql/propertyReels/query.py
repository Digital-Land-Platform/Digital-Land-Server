import strawberry
from uuid import UUID
from typing import List
from .types import ReelType
from .services import ReelService
from config.database import db

services = ReelService(db.SessionLocal())
@strawberry.type
class ReelQuery:
    @strawberry.field
    async def get_reels_by_property(self, property_id: UUID) -> List[ReelType]:
        """Get all reels for a given property.
        Args:
            property_id (UUID): The ID of the property to get reels for.
        Returns:
            List[ReelType]: A list of reels for the given property.
        """
        reels = await services.get_reels_by_property(property_id)
        return reels
