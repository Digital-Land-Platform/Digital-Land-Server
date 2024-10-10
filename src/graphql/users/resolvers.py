from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .models import User
from .schemas import CreateUserInput

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(input: CreateUserInput, db: Session):
    hashed_password = pwd_context.hash(input.password)
    user = User(name=input.name, email=input.email, password=hashed_password, role=input.role)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
