from sqlalchemy.orm import Session
from src.models.Course import Course
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import db
from sqlalchemy.future import select
from src.models.CourseCategory import CourseCategory
import uuid
from src.models.enums.ContentStatus import ContentStatus
from typing import List
from sqlalchemy import func

class CourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_course(self, course: Course) -> Course:
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
        return course

    async def get_course_by_id(self, course_id: uuid.UUID):
        stmt = select(Course).where(Course.id == course_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def update_course(self, course: Course) -> Course:
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
        return course

    async def delete_course(self, course: Course):
        await self.db.delete(course)
        await self.db.commit()
    
    async def get_category_by_id(self, category_id: uuid.UUID) -> "CourseCategory":
        result = await self.db.execute(
            select(CourseCategory).filter(CourseCategory.id == category_id)
        )
        return result.scalars().first()
    
    async def get_all_courses(self) -> List[Course]:
        """
        Fetch all courses (both Draft and Published).
        """
        async with self.db as session:
            result = await session.execute(select(Course))
            return result.scalars().all()

    async def get_courses_by_status(self, status: ContentStatus) -> List[Course]:
        """
        Fetch courses by their status (e.g., Published).
        """
        async with self.db as session:
            result = await session.execute(select(Course).filter(Course.status == status))
            return result.scalars().all()
    
    async def get_course_by_title(self, title: str):
        async with self.db as session:
            result = await session.execute(
                select(Course).where(func.lower(Course.title) == func.lower(title))
            )
            return result.scalars().first()
    
    
