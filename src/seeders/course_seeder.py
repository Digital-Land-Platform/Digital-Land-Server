import json
import os
import sys
from sqlalchemy.ext.asyncio import AsyncSession

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.models.Course import Course
from src.models.repository.CourseRepository import CourseRepository
from src.models.enums.ContentStatus import ContentStatus


class CourseSeeder:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.course_repository = CourseRepository(db)

    async def seed_courses_from_json(self):
        current_dir = os.path.dirname(__file__)

        file_path = os.path.join(current_dir, "files", "courses.json")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r") as file:
            courses = json.load(file)

        for course_data in courses:
            # Check if course already exists (e.g., by title)
            existing_course = await self.course_repository.get_course_by_title(course_data["title"])
            if existing_course:
                print(f"Course '{course_data['title']}' already exists.")
                continue

            # Create a new Course instance
            course = Course(
                title=course_data["title"],
                description=course_data.get("description"),
                category_id=course_data["category_id"],
                status=ContentStatus(course_data.get("status", "DRAFT")),
                target_audience=course_data.get("target_audience"),
                created_by=course_data.get("created_by"),
            )

            # Save to the database
            await self.course_repository.create_course(course)
            print(f"Created course: {course.title}")
