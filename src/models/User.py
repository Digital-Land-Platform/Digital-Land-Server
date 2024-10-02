from sqlalchemy import Column, String

from .Base import Base


class User(Base):
    __tablename__ = "users"
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
