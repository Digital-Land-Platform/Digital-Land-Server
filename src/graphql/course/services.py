from sqlalchemy.orm import Session
from src.models.Course import Course
from .types import CourseCreateInput, CourseUpdateInput, CourseType
from src.models.repository.CourseRepository import CourseRepository
from src.models.repository.CourseCategoryRepository import CourseCategoryRepository
from src.models.enums.CourseCategory import CourseCategory
from src.models.enums.ContentStatus import ContentStatus
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from typing import Optional, List
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException,
    NotFoundException,
    InternalServerErrorException
)

class CourseService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.course_repository = CourseRepository(db)
        self.category_repository = CourseCategoryRepository(db)
        
    async def create_course(self, course_data: CourseCreateInput) -> CourseType:
        """
        Create a new course
        Args:
            course_data (CourseCreateInput): Course data
        Returns:
            CourseType: Created course
        """
        try:
            if not (course_data.category_id):
                raise BadRequestException(detail="Category ID is required")
            
            category = await self.course_repository.get_category_by_id(course_data.category_id)
            if not category:
                raise NotFoundException(detail="Category not found")
            
            course = Course(
                title=course_data.title,
                description=course_data.description,
                category_id=category.id,
                status=ContentStatus(course_data.status),
            )
            return await self.course_repository.create_course(course)
        except (NotFoundException, BadRequestException) as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException(detail=f"Failed to create course: {e}")

    async def update_course(self, course_id: uuid.UUID, course_data: CourseUpdateInput) -> CourseType:
        """
        Update a course
        Args:
            course_id (uuid.UUID): Course ID
            course_data (CourseUpdateInput): Course data
        Returns:
            CourseType: Updated course
        """
        try:
            if not course_id:
                raise BadRequestException(detail="Course ID is required")
            
            course = await self.course_repository.get_course_by_id(course_id)
            if not course:
                raise NotFoundException(detail=f"Course with ID '{course_id}' does not exist.")
            
            if course_data.title is not None:
                course.title = course_data.title
            if course_data.description is not None:
                course.description = course_data.description
            if course_data.category_id is not None:
                category = await self.category_repository.get_category_by_id(course_data.category_id)
                if category:
                    course.category_id = category.id
                else:
                    raise NotFoundException(detail="Category not found")
            if course_data.status is not None:
                course.status = course_data.status

            return await self.course_repository.update_course(course)
        except (NotFoundException, BadRequestException) as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException(detail=f"Failed to update course: {e}")

    async def delete_course(self, course_id: uuid.UUID) -> str:
        """
        Delete a course
        Args:
            course_id (uuid.UUID): Course ID
        Returns:
            str: Deletion message
        """
        try:
            if not course_id:
                raise BadRequestException(detail="Course ID is required")
            
            course = await self.course_repository.get_course_by_id(course_id)
            if course:
                await self.course_repository.delete_course(course)
                return "Course deleted"
            raise NotFoundException(detail="Course not found")
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_all_courses(self) -> List[Course]:
        """
        Get all courses
        Returns:
            List[Course]: List of courses
        """
        try:
            return await self.course_repository.get_all_courses()
        except Exception as e:
            raise InternalServerErrorException()

    async def get_published_courses(self) -> List[Course]:
        """
        Get published courses
        Returns:
            List[Course]: List of published courses
        """
        try:
            return await self.course_repository.get_courses_by_status(ContentStatus.PUBLISHED)
        except Exception as e:
            raise InternalServerErrorException(detail=f"Failed to fetch published courses: {e}")
    
    async def get_course_by_title(self, title: str) -> Course:
        """
        Get a course by title
        Args:
            title (str): Course title
        Returns:
            Course: Course with the given title
        """
        try:
            course = await self.course_repository.get_course_by_title(title)
            if not course:
                raise NotFoundException(detail="Course not found")
            return course
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_course_by_id(self, course_id: uuid.UUID) -> Course:
        """
        Get a course by ID
        Args:
            course_id (uuid.UUID): Course ID
        Returns:
            Course: Course with the given ID
        """
        try:
            course = await self.course_repository.get_course_by_id(course_id)
            if not course:
                raise NotFoundException(detail="Course not found")
            return course
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
        