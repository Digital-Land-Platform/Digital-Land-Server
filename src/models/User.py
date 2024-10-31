from sqlalchemy import Column, String, Enum
from .UserRole import UserRole
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.models.UserProfile import UserProfile
from .Base import Base
from .Property import Property

class User(Base):
    __tablename__ = "users"
    image = Column(String)
    auth0_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(UserRole))
    
    user_profile = relationship("UserProfile", backref="users", cascade="all, delete, delete-orphan")
    
    properties = relationship("Property", back_populates="user")