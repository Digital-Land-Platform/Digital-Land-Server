import strawberry
import bcrypt

from sqlalchemy.orm import Session
from src.models import User  # Import your User model
from config.database import db  # Import your database session
from sqlalchemy.exc import IntegrityError
from src.graphql.users.types import CreateUserInput
from strawberry.types import Info

    
@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def create_user(self, info: Info, input: CreateUserInput) -> str:
        async for session in db.get_db():
            # Hash the password for security
            hashed_password = bcrypt.hashpw(input.password.encode('utf-8'), bcrypt.gensalt())
            new_user = User(name=input.name, email=input.email, password=hashed_password.decode('utf-8'), role=input.role)
            session.add(new_user)
            try:
                await session.commit()  # Commit the transaction
                return "User created successfully"
            except IntegrityError:
                await session.rollback()  # Roll back in case of error
                return "User already exists"
