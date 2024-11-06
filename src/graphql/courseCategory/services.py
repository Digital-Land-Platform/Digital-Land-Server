from src.models.CourseCategory import CourseCategory
from src.models.repository.CourseCategoryRepository import CourseCategoryRepository
from uuid import UUID
from .types import CourseCategoryType
from typing import Optional, List


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
        new_category = CourseCategory(name=name)
        return await self.category_repository.create_category(new_category)

    async def update_category(self, category_id: UUID, name: str) -> CourseCategory:
        """Update a category
        Args:
            category_id (UUID): The id of the category to update
            name (str): The new name of the category
        Returns:
            CourseCategory: The updated category
        """
        category = await self.category_repository.get_category_by_id(category_id)
        if category:
            category.name = name
            return await self.category_repository.update_category(category)
        raise Exception("Category not found")

    async def delete_category(self, category_id: UUID) -> str:
        """Delete a category
        Args:
            category_id (UUID): The id of the category to delete
        Returns:
            str: A message indicating the success of the operation
        """
        category = await self.category_repository.get_category_by_id(category_id)
        if category:
            await self.category_repository.delete_category(category)
            return "Category deleted"
        raise Exception("Category not found")
    
    async def get_all_categories(self) -> List[CourseCategory]:
        """Get all categories
        Returns
            List[CourseCategory]: A list of all categories
        """
        return await self.category_repository.get_all_categories()

    async def get_category_by_id(self, category_id: UUID) -> CourseCategory:
        """Get a category by id
        Args:
            category_id (UUID): The id of the category to get
        Returns:
            CourseCategory: The category
        """
        return await self.category_repository.get_category_by_id(category_id)
        
    async def get_category_by_name(self, name: str):
        """Get a category by name
        Args:
            name (str): The name of the category to get
        Returns:
            CourseCategory: The category
        """
        # Calls the repository method to check for an existing category by name
        return await self.category_repository.get_category_by_name(name)
    
    