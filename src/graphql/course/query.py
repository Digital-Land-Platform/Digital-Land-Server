import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .services import CourseService
from src.models.Course import Course
from src.models.enums.ContentStatus import ContentStatus
from src.models.repository.CourseRepository import CourseRepository
from typing import List
from .types import CourseType
from config.database import db
from src.middleware.AuthManagment import AuthManagement
from src.graphql.users.services import UserService
from src.models.User import UserRole
import uuid

course_service = CourseService(db)
auth_management = AuthManagement()
user_service = UserService(db.SessionLocal())

@strawberry.type
class CourseQuery:
    @strawberry.field
    async def get_published_courses(self, info) -> List[CourseType]:
        """Get all courses
        Args:
            info: Strawberry info
        Returns:
            List[CourseType]: List of courses
        """
            # Regular users can only see published courses
        return await course_service.get_published_courses()
    
    @strawberry.field
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions 
    async def get_courses_by_status(self, status: ContentStatus) -> List[CourseType]:
        return await course_service.get_courses_by_status(status)
    
    @strawberry.field
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions 
    async def get_all_courses(self) -> List[CourseType]:
        """Get all courses
        Args:
            info: Strawberry info
        Returns:
            List[CourseType]: List of courses
        """
        return await course_service.get_all_courses()
    