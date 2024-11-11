import strawberry
from src.graphql.courseContent.services import CourseContentService
from src.graphql.courseContent.types import CourseContentCreateInput, CourseContentUpdateInput, CourseContentType
from typing import List
import uuid
from config.database import db


# Initialize the CourseContentService with the database session outside the resolver
course_content_service = CourseContentService(db.SessionLocal())

@strawberry.type
class CourseContentMutation:
    @strawberry.mutation
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
    async def delete_content(self, content_id: uuid.UUID) -> str:
        """Delete content
        Args:
            content_id (uuid.UUID): Content ID
        Returns:
            str: Deletion message
        """
        return await course_content_service.delete_content(content_id)

