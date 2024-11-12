import strawberry
from .services import CourseService
from .types import CourseCreateInput, CourseUpdateInput, CourseType
from config.database import db
import uuid
from src.middleware.AuthManagment import AuthManagement
from src.graphql.users.services import UserService
from src.models.User import UserRole

course_service = CourseService(db.SessionLocal())
auth_management = AuthManagement()
user_service = UserService(db.SessionLocal())

@strawberry.type
class CourseMutation:
    @strawberry.mutation
    #@auth_management.role_required([UserRole.ADMIN])
    async def create_course(self, course_data: CourseCreateInput, info: strawberry.types.info) -> CourseType:
        """Create a new course
        Args:
            course_data (CourseCreateInput): Course data
        Returns:
            CourseType: Created course
        """
        #token = info.context["request"].headers.get("authorization").split(" ")[1]
        #Get user info from token
        #user_info = auth_management.get_user_info(token)  
        #Retrieve the user from the database using the email obtained from the token
        #user = await user_service.get_user_by_email(user_info.get("email"))
        existing_course = await course_service.get_course_by_title(course_data.title)
        if existing_course:
            raise Exception(f"Course with title '{course_data.title}' already exists.")
        
        return await course_service.create_course(course_data)

    @strawberry.mutation
    #@auth_management.role_required([UserRole.ADMIN])
    async def update_course(self, course_id: uuid.UUID, course_data: CourseUpdateInput, info: strawberry.types.info) -> CourseType:
        """Update a course
        Args:
            course_id (uuid.UUID): Course ID
            course_data (CourseUpdateInput): Course data
        Returns:
            CourseType: Updated course
        """
        #token = info.context["request"].headers.get("authorization").split(" ")[1]
        #Get user info from token
        #user_info = auth_management.get_user_info(token)  
        #Retrieve the user from the database using the email obtained from the token
        #user = await user_service.get_user_by_email(user_info.get("email"))
        course = await course_service.get_course_by_id(course_id)
        if not course:
            raise Exception(f"Course with ID '{course_id}' does not exist.")

        

        # Save updated course
        return await course_service.update_course(course_id, course_data)   

    @strawberry.mutation
    #@auth_management.role_required([UserRole.ADMIN])
    async def delete_course(self, course_id: uuid.UUID, info: strawberry.types.info) -> str:
        """Delete a course
        Args:
            course_id (uuid.UUID): Course ID
        Returns:
            str: Deletion message
        """
        #token = info.context["request"].headers.get("authorization").split(" ")[1]
        #Get user info from token
        #user_info = auth_management.get_user_info(token)  
        #Retrieve the user from the database using the email obtained from the token
        #user = await user_service.get_user_by_email(user_info.get("email"))
        course = await course_service.get_course_by_id(course_id)
        if not course:
            raise Exception(f"Course with ID '{course_id}' not found.")
        return await course_service.delete_course(course_id)
