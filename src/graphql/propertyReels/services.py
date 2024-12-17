# GLOBAL IMPORTS
from src.utils.globalVariables.globalConstant import max_duration, max_size

# OTHER IMPORTS
from src.models.Reel import Reel
from uuid import UUID
from src.models.repository.PropertyReelsRepository import ReelRepository
from src.models.repository.propertyRepository import PropertyRepository
from sqlalchemy.ext.asyncio import AsyncSession
import cloudinary
from cloudinary.uploader import upload
from cloudinary import uploader
from strawberry.file_uploads import Upload
from typing import List
from src.utils.utility import Utility
from .types import ReelCreateInput, ReelUpdateInput
import moviepy.editor as mp
from pathlib import Path
from io import BytesIO
import tempfile
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException, InternalServerErrorException, 
    NotFoundException, UnauthorizedException
)


class ReelService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.reel_repository = ReelRepository(db)
        self.property_repository = PropertyRepository(db)

    async def validate_video(self, file: Upload) -> None:
        """Validate the uploaded video file."""
        # Check if the file is in MP4 format
        if not file.filename.endswith(".mp4"):
            raise BadRequestException("Invalid file format. Please upload an MP4 file.")
        
       
        file_data = await file.read()  
        
        # Check the file size (e.g., max 10 MB)
        # max_size = 20 * 1024 * 1024  # 10 MB
        if len(file_data) > max_size:
            raise BadRequestException("File size exceeds the 10 MB limit.")
        
        
        # Create a temporary file to load and validate the video
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(file_data)
            temp_file_path = temp_file.name
        
        video_file = BytesIO(file_data)
        try:
            video_clip = mp.VideoFileClip(temp_file_path)
            # max_duration = 60  
            if video_clip.duration > max_duration:
                raise BadRequestException(f"Video duration exceeds the {max_duration} seconds limit.")
        finally:
            video_file.close()
        
        # Reset the file pointer to the beginning of the file    
        file.file.seek(0)

    async def upload_video_to_cloudinary(self, file: Upload) -> str:
        """Upload the video file to Cloudinary and return the URL.
        Args:
            file (Upload): The uploaded video file.
        Returns:
            str: The URL of the uploaded video.
        """
        try:
            await self.validate_video(file)
            
            # Upload the video to Cloudinary
            upload_result = cloudinary.uploader.upload(file.file, resource_type="video")
            return upload_result.get('secure_url')
        except cloudinary.exceptions.Error as e:
            Utility.print_red(f"Cloudinary error: {e}")
            raise InternalServerErrorException("Failed to upload video, Try again later.")
        

    async def create_reel(self, property_id: UUID, reel_data: ReelCreateInput) -> Reel:
        """Create a new reel for a property.
        Args:
            property_id (UUID): The ID of the property.
            reel_data (ReelCreateInput): The data to create the reel.
        Returns:
            Reel: The created reel.
        """
        
        property = await self.property_repository.get_property(property_id)
        if not property:
            raise NotFoundException("Property not found")
    
        file = reel_data.file
        title = reel_data.title
        description = reel_data.description
        creator_id = property.user_id
        
        try:
            # Check if the property already has the max number of reels
            if not await self.reel_repository.check_reel_limit(property_id):
                raise BadRequestException("Property has reached the maximum number of reels")

            # Upload video and get URL
            video_url = await self.upload_video_to_cloudinary(file)

            # Create and save the new reel
            reel = Reel(
                property_id=property_id,
                creator_id=creator_id,
                title=title,
                description=description,
                url=video_url
            )
            return await self.reel_repository.create_reel(reel)
        except BadRequestException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()

    async def update_reel(self, reel_id: UUID, reel_data: ReelUpdateInput) -> Reel:
        """Update an existing reel.
        Args:
            reel_id (UUID): The ID of the reel to update.
            reel_data (ReelUpdateInput): The data to update the reel.
        Returns:
            Reel: The updated reel.
        """
        # Retrieve the existing reel
        reel = await self.reel_repository.get_reel_by_id(reel_id)
        if not reel:
            raise NotFoundException("Reel not found")

        # Validate that the current user is the creator of the reel
        if reel.creator_id != reel_data.creator_id:
            raise UnauthorizedException("You do not have permission to update this reel")
        
        # Only update the fields that were provided
        if reel_data.title:
            reel.title = reel_data.title
        if reel_data.description:
            reel.description = reel_data.description

        if reel_data.file:
            try:
                await self.validate_video(reel_data.file)
                
                old_public_id = reel.url.split('/')[-1].split('.')[0]
                # Delete the old video from Cloudinary
                uploader.destroy(old_public_id, resource_type="video")

            # Upload the new video to Cloudinary
                new_video_url = await self.upload_video_to_cloudinary(reel_data.file)
                reel.url = new_video_url
            except (NotFoundException, UnauthorizedException) as e:
                raise e
            except Exception as e:
                raise InternalServerErrorException

        # Update the reel in the database
        return await self.reel_repository.update_reel(reel)

    async def get_reels_by_property(self, property_id: UUID) -> List[Reel]:
        # This is a bug, property has to be checked for confiming its existance
        return await self.reel_repository.get_reels_by_property(property_id)

    async def delete_reel(self, reel_id: UUID, creator_id: UUID) -> None:
        """Delete an existing reel.
        Args:
            reel_id (UUID): The ID of the reel to delete.
        Returns:
            bool: True if the reel was deleted successfully.
        """
        reel = await self.reel_repository.get_reel_by_id(reel_id)
        if not reel:
            raise NotFoundException("Reel not found")
        
        if reel.creator_id != creator_id:
            raise UnauthorizedException("You do not have permission to delete this reel")

        try:
            public_id = reel.url.split('/')[-1].split('.')[0]
            uploader.destroy(public_id, resource_type="video")
        except Exception as e:
            raise InternalServerErrorException()

        await self.reel_repository.delete_reel(reel)
        return True
    