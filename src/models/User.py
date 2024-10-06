from sqlalchemy import Column, String, Enum
from .UserRole import UserRole
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.models.UserProfile import UserProfile
from sqlalchemy.orm import relationship
from src.models.UserProfile import UserProfile
from .Base import Base


class User(Base):
    __tablename__ = "users"
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(UserRole))
    user_profile = relationship("UserProfile", backref="users", cascade="all, delete, delete-orphan")

    properties = relationship("Property", back_populates="owner")