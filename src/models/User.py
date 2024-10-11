from .Base import Base
from sqlalchemy import Column, String, Enum as SQLAlchemyEnum
import strawberry
from enum import Enum

# Define the UserRole enum using Strawberry's Enum
@strawberry.enum
class UserRole(Enum):
    LAND_OWNER = "Land Owner"
    BUYER = "Buyer"
    NOTARY = "Notary"
    ADMIN = "Admin"

class User(Base):
    __tablename__ = "users"
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role: UserRole = Column(SQLAlchemyEnum(UserRole))
