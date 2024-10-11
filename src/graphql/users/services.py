from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User

class UserService:
    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
        result = await session.get(User, user_id)
        return result

    @staticmethod
    async def create_user(name: str, email: str, password: str, role: str, session: AsyncSession):
        new_user = User(name=name, email=email, password=password, role=role)
        session.add(new_user)
        await session.commit()  # Commit the transaction
