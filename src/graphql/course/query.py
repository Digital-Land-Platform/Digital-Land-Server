import strawberry
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
    async def get_courses(self, info) -> List[CourseType]:
        """Get all courses
        Args:
            info: Strawberry info
        Returns:
            List[CourseType]: List of courses
        """
        # Get the 'Authorization' header
        authorization_header = info.context["request"].headers.get("authorization")

        # Check if the 'Authorization' header exists
        if not authorization_header:
            raise Exception("Authorization header missing in request")

        # Safely split the token
        try:
            token = authorization_header.split(" ")[1]
        except IndexError:
            raise Exception("Invalid authorization format")

        # Proceed with user information retrieval and role check
        user_info = auth_management.get_user_info(token)
        user = await user_service.get_user_by_email(user_info.get("email"))

        if user.role == UserRole.ADMIN:
            # Admins can see all courses
            return await course_service.get_all_courses()
        else:
            # Regular users can only see published courses
            return await course_service.get_published_courses()
    @strawberry.field
    async def courses(self) -> List[CourseType]:
        # Fetch only the courses marked as "PUBLISHED"
        return await course_service.get_courses_by_status("PUBLISHED")