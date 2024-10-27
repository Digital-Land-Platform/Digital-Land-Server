import strawberry
from uuid import UUID
from typing import Optional
from src.models.Amenities import Amenities
from src.models.User import UserRole
from src.graphql.amenity.index import AmenitiesType, AmenityInput, AmenityUpdateInput
from config.database import db
from src.graphql.users.services import UserService
from src.graphql.property.services import PropertyService
from src.middleware.AuthManagment import AuthManagement
from .services import AmenityService

# Initialize the services required for property mutations
amenity_service = AmenityService(db.SessionLocal())
auth_management = AuthManagement()
user_service = UserService(db.SessionLocal())

@strawberry.type
class AmenityMutation:
    @strawberry.mutation
    @auth_management.role_required([UserRole.ADMIN])
    async def create_amenity(self, amenity_input: list[AmenityInput], info: strawberry.types.info) -> list[AmenitiesType]:
        """
        Create a new amenity. Only users with the role of ADMIN are allowed.

        Args:
            menity_input (AmenityInput): The details of the amenity to create.

        Returns:
            Amenities: The created amenity object.
        """
        try:
            token = info.context["request"].headers.get("authorization").split(" ")[1]
            # Get user info from token
            user_info = auth_management.get_user_info(token)
            
            # Retrieve the user from the database using the email obtained from the token
            user = await user_service.get_user_by_email(user_info.get("email"))
            
            created_amenities = []
            for amenity in amenity_input:
                # Create the new amenity instance using the input details
                new_amenity = Amenities(title=amenity.title, icon=amenity.icon)  # Assuming the `name` is the title
                created_amenity = await amenity_service.create_amenity(new_amenity)
                created_amenities.append(AmenitiesType(title=created_amenity.title, icon=created_amenity.icon))
            # Return the created amenity
            return created_amenities
        except Exception as e:
            raise Exception(f"Failed to create amenity: {e}")
    
    @strawberry.mutation
    @auth_management.role_required([UserRole.ADMIN])
    async def update_amenity(
        self,
        amenity_update_input: list[AmenityUpdateInput],
        info: strawberry.types.info
    ) -> list[AmenitiesType]:
        """
        Update multiple amenities in a single call. Only users with the role of ADMIN are allowed.

        Args:
            amenity_id (UUID): The ID of the amenity to update.
            amenity_update_input (AmenityInput): The updated details of the amenity.

        Returns:
            AmenitiesType: The updated amenity object.
        """
        updated_amenities = []
        try:
            # Extract the token and get user info
            token = info.context["request"].headers.get("authorization").split(" ")[1]
            user_info = auth_management.get_user_info(token)

            # Check if the user is authorized
            user = await user_service.get_user_by_email(user_info.get("email"))

            for amenity_update in amenity_update_input:
                #Save the updated amenity
                updated_amenity = await amenity_service.update_amenity(amenity_update.amenity_id, amenity_update)
                updated_amenities.append(AmenitiesType(
                    title=updated_amenity.title,
                    icon=updated_amenity.icon
            ))
        except Exception as e:
            raise Exception(f"Failed to update amenity: {e}")
        return updated_amenities
        
    @strawberry.mutation
    @auth_management.role_required([UserRole.ADMIN])   
    async def delete_amenity(self, amenity_id: UUID, info) -> bool:
        """
        Delete an amenity.
        
        Args:
            amenity_id (UUID): The id of the amenity to be deleted.
            
        Returns:
            bool: True if the amenity was deleted successfully, False otherwise.
        """
        
        try:
            token = info.context["request"].headers.get("authorization").split(" ")[1]
            user_info = auth_management.get_user_info(token)

            # Check if the user is authorized
            user = await user_service.get_user_by_email(user_info.get("email"))

            result = await amenity_service.delete_amenity(amenity_id)
            return result
        except Exception as e:
            raise Exception(f"Failed to delete amenity: {e}")
    