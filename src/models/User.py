from sqlalchemy import Column, String, Enum
from .UserRole import UserRole
from sqlalchemy import Column, String

from .Base import Base


class User(Base):
    __tablename__ = "users"
    image = Column(String)
    auth0_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(UserRole))
