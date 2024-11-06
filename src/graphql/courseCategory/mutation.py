import strawberry
from .services import CourseCategoryService
from .types import CourseCategoryCreateInput, CourseCategoryType, CourseCategoryUpdateInput
from config.database import db
from uuid import UUID
from src.models.User import UserRole
from src.middleware.AuthManagment import AuthManagement
from src.graphql.users.services import UserService

category_service = CourseCategoryService(db.SessionLocal())
auth_management = AuthManagement()
user_service = UserService(db.SessionLocal())

@strawberry.type
class CourseCategoryMutation:
    @strawberry.mutation
    @auth_management.role_required([UserRole.ADMIN])
    async def create_category(self, name: str, info: strawberry.types.info) -> CourseCategoryType:
        """Create a new category
        Args:
            name (str): The name of the category
        Returns:
            CourseCategoryType: The created category
        """
        token = info.context["request"].headers.get("authorization").split(" ")[1]
        #Get user info from token
        user_info = auth_management.get_user_info(token)  
        #Retrieve the user from the database using the email obtained from the token
        user = await user_service.get_user_by_email(user_info.get("email"))
        existing_category = await category_service.get_category_by_name(name)
        if existing_category:
            raise Exception(f"Category with name '{name}' already exists.")
        
        return await category_service.create_category(name)

    @strawberry.mutation
    @auth_management.role_required([UserRole.ADMIN])
    async def update_category(self, category_id: UUID, name: str, info: strawberry.types.info) -> CourseCategoryType:
        """Update a category
        Args:
        
            category_id (UUID): The id of the category to update
            name (str): The new name of the category
        Returns:
            CourseCategoryType: The updated category
        """
        token = info.context["request"].headers.get("authorization").split(" ")[1]
        #Get user info from token
        user_info = auth_management.get_user_info(token)  
        #Retrieve the user from the database using the email obtained from the token
        user = await user_service.get_user_by_email(user_info.get("email"))
        return await category_service.update_category(category_id, name)

    @strawberry.mutation
    @auth_management.role_required([UserRole.ADMIN])
    async def delete_category(self, category_id: UUID, info: strawberry.types.info) -> str:
        """Delete a category
        Args:
            category_id (UUID): The id of the category to delete
        Returns:
            str: A message indicating the success of the operation
        """
        token = info.context["request"].headers.get("authorization").split(" ")[1]
        #Get user info from token
        user_info = auth_management.get_user_info(token)  
        #Retrieve the user from the database using the email obtained from the token
        user = await user_service.get_user_by_email(user_info.get("email"))
        return await category_service.delete_category(category_id)
