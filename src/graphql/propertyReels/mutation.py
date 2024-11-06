import strawberry
from uuid import UUID
from .services import ReelService
from typing import List, Optional
from .types import ReelType
import cloudinary.uploader
from config.database import db
from strawberry.file_uploads import Upload
from .types import ReelCreateInput, ReelType, ReelUpdateInput

services = ReelService(db.SessionLocal())

@strawberry.type
class ReelMutation:
    @strawberry.mutation
    async def create_reel(self, property_id: UUID, reel_data: ReelCreateInput) -> ReelType:
        """Create a new reel.
        Args:
            property_id (UUID): The ID of the property the reel belongs to.
            reel_data (ReelCreateInput): The data to create the reel.
        Returns:
            Reel: The created reel.
        """
        reel = await services.create_reel(property_id, reel_data)

        # Call the service method to create the reel
        return ReelType(
            id=reel.id,
            property_id=reel.property_id,
            creator_id=reel.creator_id,
            title=reel.title,
            description=reel.description,
            url=reel.url,
        )
    
    @strawberry.mutation
    async def update_reel(
        self, 
        reel_id: UUID, 
        reel_data: ReelUpdateInput,
    ) -> ReelType:
        
        """Update an existing reel.
        Args:
            reel_id (UUID): The ID of the reel to update.
            reel_data (ReelUpdateInput): The data to update the reel.
        Returns:
            Reel: The updated reel.
        """
        updated_reel = await services.update_reel(reel_id, reel_data)

        # Return the updated Reel as ReelType
        return ReelType(
            id=updated_reel.id,
            property_id=updated_reel.property_id,
            creator_id=updated_reel.creator_id,
            title=updated_reel.title,
            description=updated_reel.description,
            url=updated_reel.url,
        )


    @strawberry.mutation
    async def delete_reel(self, reel_id: UUID, creator_id: UUID) -> bool:
        """Delete a reel by its ID.
        Args:
            reel_id (UUID): The ID of the reel to delete.
        Returns:
            bool: True if the reel was deleted successfully, False otherwise.
        """
        return await services.delete_reel(reel_id, creator_id)

    @strawberry.mutation
    async def get_reel(self, reel_id: UUID) -> ReelType:
        """Get a reel by its ID
        Args:
            reel_id (UUID): The ID of the reel to retrieve
        Returns:
            ReelType: The retrieved reel
        """
        reel = await services.get_reel_by_id(reel_id)

        # Return the retrieved Reel as ReelType
        return ReelType(
            id=reel.id,
            property_id=reel.property_id,
            creator_id=reel.creator_id,
            title=reel.title,
            description=reel.description,
            url=reel.url,
        )