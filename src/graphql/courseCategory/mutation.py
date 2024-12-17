import strawberry
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException, CustomException
)
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .services import CourseCategoryService
from .types import CourseCategoryType
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
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def create_category(self, name: str, info: strawberry.types.info) -> CourseCategoryType:
        """Create a new category
        Args:
            name (str): The name of the category
        Returns:
            CourseCategoryType: The created category
        """
        if not name or name is None:
            raise BadRequestException("Category name is required.")
        
        existing_category = await category_service.get_category_by_name(name)
        if existing_category:
            raise CustomException(status_code=409, detail=f"Category with name '{name}' already exists.")
        
        return await category_service.create_category(name)

    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def update_category(self, category_id: UUID, name: str, info: strawberry.types.info) -> CourseCategoryType:
        """Update a category
        Args:
        
            category_id (UUID): The id of the category to update
            name (str): The new name of the category
        Returns:
            CourseCategoryType: The updated category
        """
        return await category_service.update_category(category_id, name)

    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def delete_category(self, category_id: UUID, info: strawberry.types.info) -> str:
        """Delete a category
        Args:
            category_id (UUID): The id of the category to delete
        Returns:
            str: A message indicating the success of the operation
        """
        return await category_service.delete_category(category_id)
