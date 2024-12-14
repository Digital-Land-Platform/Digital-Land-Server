import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from src.models.User import UserRole
from src.middleware.AuthManagment import AuthManagement
from src.graphql.courseContent.services import CourseContentService
from src.graphql.courseContent.types import CourseContentCreateInput, CourseContentUpdateInput, CourseContentType
from typing import List
import uuid
from config.database import db

auth_management = AuthManagement()
course_content_service = CourseContentService(db.SessionLocal())

@strawberry.type
class CourseContentMutation:
    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def create_content(self, course_id: uuid.UUID, content_data: CourseContentCreateInput) -> CourseContentType:
        """Create content
        Args:
            course_id (uuid.UUID): Course ID
            content_data (CourseContentCreateInput): Content data
        Returns:
            CourseContentType: Created course content
        """
        return await course_content_service.create_content(course_id, content_data)

    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def update_content(self, content_id: uuid.UUID, content_data: CourseContentUpdateInput) -> CourseContentType:
        """Update content
        Args:
            content_id (uuid.UUID): Content ID
            content_data (CourseContentUpdateInput): Content data
        Returns:
            CourseContentType: Updated course content
        """
        return await course_content_service.update_content(content_id, content_data)

    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def delete_content(self, content_id: uuid.UUID) -> str:
        """Delete content
        Args:
            content_id (uuid.UUID): Content ID
        Returns:
            str: Deletion message
        """
        return await course_content_service.delete_content(content_id)

