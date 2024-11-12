from sqlalchemy.orm import Session
from src.models.Course import Course
from .types import CourseCreateInput, CourseUpdateInput, CourseType
from src.models.repository.CourseRepository import CourseRepository
from src.models.repository.CourseCategoryRepository import CourseCategoryRepository
from src.models.enums.CourseCategory import CourseCategory
from src.models.enums.ContentStatus import ContentStatus
#from src.models.enums.CourseStatus import CourseStatus
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from typing import Optional, List


class CourseService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.course_repository = CourseRepository(db)
        self.category_repository = CourseCategoryRepository(db)
        
    async def create_course(self, course_data: CourseCreateInput) -> CourseType:
        """Create a new course
        Args:
            course_data (CourseCreateInput): Course data
        Returns:
            CourseType: Created course
        """
        category = await self.course_repository.get_category_by_id(course_data.category_id)

        if not category:
            raise Exception("Category not found")
        
        course = Course(
            title=course_data.title,
            description=course_data.description,
            category_id=category.id,
            status=ContentStatus(course_data.status),
        )
        return await self.course_repository.create_course(course)

    async def update_course(self, course_id: uuid.UUID, course_data: CourseUpdateInput) -> CourseType:
        """Update a course
        Args:
            course_id (uuid.UUID): Course ID
            course_data (CourseUpdateInput): Course data
        Returns:
            CourseType: Updated course
        """
        course = await self.course_repository.get_course_by_id(course_id)
        
        if not course:
            raise Exception(f"Course with ID '{course_id}' does not exist.")
        
        if course_data.title is not None:
            course.title = course_data.title
        if course_data.description is not None:
            course.description = course_data.description
        if course_data.category_id is not None:
            category = await self.category_repository.get_category_by_id(course_data.category_id)
            if category:
                course.category_id = category.id
            else:
                raise Exception("Category not found")
        if course_data.status is not None:
            course.status = course_data.status
            #if course_data.target_audience is not None:
                #course.target_audience = course_data.target_audience
        return await self.course_repository.update_course(course)
        raise Exception("Course not found")

    async def delete_course(self, course_id: uuid.UUID) -> str:
        """Delete a course
        Args:
            course_id (uuid.UUID): Course ID
        Returns:
            str: Deletion message
        """
        course = await self.course_repository.get_course_by_id(course_id)
        if course:
            await self.course_repository.delete_course(course)
            return "Course deleted"
        raise Exception("Course not found")
    
    async def get_all_courses(self) -> List[Course]:
        """Get all courses
        Returns:
            List[Course]: List of courses
        """
        # Return all courses, including drafts and published courses
        return await self.course_repository.get_all_courses()

    async def get_published_courses(self) -> List[Course]:
        """Get published courses
        Returns:
            List[Course]: List of published courses
        """
        # Return only published courses
        return await self.course_repository.get_courses_by_status(ContentStatus.PUBLISHED)
    
    async def get_course_by_title(self, title: str):
        """Get a course by title
        Args:
            title (str): Course title
        Returns:
            Course: Course with the given title
        """
        return await self.course_repository.get_course_by_title(title)
    
    async def get_course_by_id(self, course_id: uuid.UUID):
        """Get a course by ID
        Args:
            course_id (uuid.UUID): Course ID
        Returns:
            Course: Course with the given ID
        """
        # This calls the repository method
        return await self.course_repository.get_course_by_id(course_id)