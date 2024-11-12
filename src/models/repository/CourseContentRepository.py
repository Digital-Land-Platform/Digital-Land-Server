from sqlalchemy.ext.asyncio import AsyncSession
from src.models.CourseContent import CourseContent
from uuid import UUID
from sqlalchemy.future import select
from typing import Optional, List
from src.models.enums.ContentType import ContentType

class CourseContentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_content(self, content: CourseContent) -> "CourseContent":
        """Create content
        Args:
            content (CourseContent): Course content
        Returns:
            CourseContent: Created course content
        """
        self.db.add(content)
        await self.db.commit()
        await self.db.refresh(content)
        return content

    async def get_content_by_id(self, content_id: UUID) -> CourseContent:
        """Get content by ID
        Args:
            content_id (UUID): Content ID
        Returns:
            CourseContent: Course content
        """
        async with self.db as session:
            # Query the database to find the content by id
            result = await session.execute(
            select(CourseContent).where(CourseContent.id == content_id)
            )
            return result.scalars().first()

    async def update_content(self, content: CourseContent) -> "CourseContent":
        """Update content
        Args:
            content (CourseContent): Course content
        Returns:
            CourseContent: Updated course content
        """
        
        self.db.add(content)
        await self.db.commit()
        await self.db.refresh(content)
        return content

    async def delete_content(self, content: CourseContent) -> None:
        """Delete content
        Args:
            content (CourseContent): Course content
        """
        await self.db.delete(content)
        await self.db.commit()
    
    async def get_content_by_course_and_title(self, course_id: UUID, title: str):
        """Get content by course and title
        Args:
            course_id (UUID): Course ID
            title (str): Content title
        Returns:
            CourseContent: Course content
        """
        async with self.db as session:
            result = await session.execute(
                select(CourseContent).filter(
                    CourseContent.course_id == course_id, 
                    func.lower(CourseContent.title) == func.lower(title)
                )
        )
            return result.scalars().first()
    
        # In your repository class
    async def get_all_contents(self) -> List[CourseContent]:
        """Get all contents
        Returns:
            List[CourseContent]: List of all course contents
        """
        async with self.db as session:
            result = await session.execute(select(CourseContent))
            return result.scalars().all()  # Returns a list of all CourseContent objects



