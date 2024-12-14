from sqlalchemy.ext.asyncio import AsyncSession
from src.models.CourseCategory import CourseCategory
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy import func

class CourseCategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_category(self, category: CourseCategory) -> CourseCategory:
        """
        Create a new category in the database.
        """
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def get_category_by_id(self, category_id: UUID) -> CourseCategory:
        """
        Fetch a category by its ID.
        """
        query = select(CourseCategory).where(CourseCategory.id == category_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def update_category(self, category: CourseCategory) -> CourseCategory:
        """
        Update a category in the database.
        """
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete_category(self, category: CourseCategory) -> None:
        """
        Delete a category from the database.
        """
        await self.db.delete(category)
        await self.db.commit()

    async def get_category_by_name(self, name: str):
        """
        Fetch a category by its name.
        """
        async with self.db as session:
            result = await session.execute(
                select(CourseCategory).filter(func.lower(CourseCategory.name) == func.lower(name))
            )
            return result.scalars().first()
    
    async def get_all_categories(self) -> list:
        """
        Fetch all categories from the database.
        """
        async with self.db as session:
            # Query the database to get all categories
            result = await session.execute(select(CourseCategory))
            return result.scalars().all()
        