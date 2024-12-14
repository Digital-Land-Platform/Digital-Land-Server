from src.models.CourseCategory import CourseCategory
from src.models.repository.CourseCategoryRepository import CourseCategoryRepository
from uuid import UUID
from .types import CourseCategoryType
from typing import Optional, List
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException,
    NotFoundException,
    InternalServerErrorException,
    CustomException,
)

class CourseCategoryService:
    def __init__(self, db):
        self.category_repository = CourseCategoryRepository(db)
    
    async def create_category(self, name: str) -> CourseCategory:
        """Create a new category
        Args:
            name (str): The name of the category
        Returns:
            CourseCategory: The created category
        """
        try:
            new_category = CourseCategory(name=name)
            return await self.category_repository.create_category(new_category)
        except Exception as e:
            raise InternalServerErrorException()

    async def update_category(self, category_id: UUID, name: str) -> CourseCategory:
        """Update a category
        Args:
            category_id (UUID): The id of the category to update
            name (str): The new name of the category
        Returns:
            CourseCategory: The updated category
        """
        try:
            category = await self.category_repository.get_category_by_id(category_id)
            if category:
                category.name = name
                return await self.category_repository.update_category(category)
            raise NotFoundException(detail="Category not found")
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()

    async def delete_category(self, category_id: UUID) -> str:
        """Delete a category
        Args:
            category_id (UUID): The id of the category to delete
        Returns:
            str: A message indicating the success of the operation
        """
        try:
            category = await self.category_repository.get_category_by_id(category_id)
            if category:
                await self.category_repository.delete_category(category)
                return "Category deleted"
            raise NotFoundException(detail="Category not found")
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_all_categories(self) -> List[CourseCategory]:
        """Get all categories
        Returns
            List[CourseCategory]: A list of all categories
        """
        try:
            return await self.category_repository.get_all_categories()
        except Exception as e:
            raise InternalServerErrorException()

    async def get_category_by_id(self, category_id: UUID) -> CourseCategory:
        """Get a category by id
        Args:
            category_id (UUID): The id of the category to get
        Returns:
            CourseCategory: The category
        """
        try:
            category = await self.category_repository.get_category_by_id(category_id)
            if not category:
                raise NotFoundException(detail="Category not found")
            return category
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
        
    async def get_category_by_name(self, name: str) -> CourseCategory:
        """Get a category by name
        Args:
            name (str): The name of the category to get
        Returns:
            CourseCategory: The category
        """
        try:
            category = await self.category_repository.get_category_by_name(name)
            if not category:
                raise NotFoundException(detail="Category not found")
            return category
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()