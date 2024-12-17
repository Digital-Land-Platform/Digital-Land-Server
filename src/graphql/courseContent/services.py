from src.models.repository.CourseContentRepository import CourseContentRepository
from src.graphql.courseContent.types import CourseContentCreateInput, CourseContentUpdateInput
from src.models.CourseContent import CourseContent
from src.models.enums.ContentType import ContentType
from .types import CourseContentType
from uuid import UUID
import uuid
import cloudinary
from typing import List
from strawberry.file_uploads import Upload
from sqlalchemy.ext.asyncio import AsyncSession
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException,
    NotFoundException,
    InternalServerErrorException,
    CustomException,
)

class CourseContentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = CourseContentRepository(db)
        
    async def upload_video(self, file: Upload) -> str:
        """
        Handles video upload to Cloudinary and returns the video URL.
        """
        try:
            # Upload the video to Cloudinary
            upload_result = cloudinary.uploader.upload(file.file, resource_type="video")
            video_url = upload_result.get('secure_url')
            return video_url
        except Exception as e:
            raise InternalServerErrorException()

    async def create_content(self, course_id: UUID, content_data: CourseContentCreateInput) -> "CourseContentType":
        """
        Create content
        Args:
            course_id (UUID): Course ID
            content_data (CourseContentCreateInput): Content data
        Returns:
            CourseContentType: Created course content
        """
        try:
            existing_content = await self.repository.get_content_by_course_and_title(course_id, content_data.title)
            if existing_content:
                raise CustomException(status_code=409, detail=f"Content of type {content_data.content_type} already exists for this course.")

            # Determine which field to populate based on the content type
            content_url = None
            text_content = None
            
            if content_data.content_type == ContentType.VIDEO or content_data.content_type == ContentType.REEL:
                if content_data.file:
                    content_url = await self.upload_video(content_data.file)
                    
            elif content_data.content_type == ContentType.ARTICLE or content_data.content_type == ContentType.QUIZ:
                text_content = content_data.text_content

            # Create a new content instance from the provided input data
            content = CourseContent(
                course_id=course_id,
                content_type=content_data.content_type,
                title=content_data.title,
                content_url=content_url,
                text_content=text_content,
            )

            return await self.repository.create_content(content)
        except (CustomException, BadRequestException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()

    async def update_content(self, content_id: UUID, content_data: CourseContentUpdateInput) -> "CourseContentType":
        """
        Update content
        Args:
            content_id (UUID): Content ID
            content_data (CourseContentUpdateInput): Content data
        Returns:
            CourseContentType: Updated course content
        """
        try:
            # Retrieve content by ID
            content = await self.repository.get_content_by_id(content_id)
            if not content:
                raise NotFoundException(detail="Content not found")
            
            if content_data.content_type is not None:
                content.content_type = content_data.content_type
                
                if content.content_type in {ContentType.VIDEO, ContentType.REEL}:
                    if content_data.file:
                        if content.content_url:
                            public_id = content.content_url.split('/')[-1].split('.')[0]
                            cloudinary.uploader.destroy(public_id, resource_type="video")
                            
                        content.content_url = await self.upload_video(content_data.file)
                        content.text_content = None  # Clear text content if not applicable
                    
                elif content.content_type in {ContentType.ARTICLE, ContentType.QUIZ}:
                    content.text_content = content_data.text_content if content_data.text_content is not None else content.text_content
                    content.content_url = None  # Clear URL if not applicable
            content.title = content_data.title or content.title if content_data.title is not None else content.title       
            return await self.repository.update_content(content)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()

    async def delete_content(self, content_id: UUID) -> str:
        """
        Delete content
        Args:
            content_id (UUID): Content ID
        Returns:
            str: Deletion message
        """
        try:
            # Retrieve content by ID
            content = await self.repository.get_content_by_id(content_id)
            if not content:
                raise NotFoundException(detail="Content not found")
            if content.content_url:
                try:
                    public_id = content.content_url.split('/')[-1].split('.')[0]
                    result = cloudinary.uploader.destroy(public_id, resource_type="video")
                    
                    if result['result'] == 'ok':
                        print("Video deleted from Cloudinary")
                except Exception as e:
                    raise InternalServerErrorException(detail=f"Error deleting video from Cloudinary: {e}")
            await self.repository.delete_content(content)
            return "Content deleted"
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_content_by_id(self, content_id: uuid.UUID) -> CourseContentType:
        """
        Get content by ID
        Args:
            content_id (uuid.UUID): Content ID
        Returns:
            CourseContentType: Course content
        """
        try:
            content = await self.repository.get_content_by_id(content_id)
            if not content:
                raise NotFoundException(detail="Content not found")
            return CourseContentType(
                id=content.id,
                content_type=content.content_type,
                content_url=content.content_url,
                text_content=content.text_content,
                title=content.title
            )
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_all_contents(self, course_id: uuid.UUID) -> List[CourseContentType]:
        """
        Get all contents
        Returns:
            List[CourseContentType]: List of course contents
        """

        # THIS SERVICE HAS TO BE REFACTORED TO GET ALL CONTENTS FOR A SPECIFIC COURSE
        try:
            contents = await self.repository.get_all_contents()
        
            if not contents:
                raise NotFoundException(detail="No content found")
        
            # Map each content to the CourseContentType and return the list
            return [
                CourseContentType(
                    id=content.id,
                    content_type=content.content_type,
                    content_url=content.content_url,
                    text_content=content.text_content,
                    title=content.title
                ) for content in contents
            ]
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()