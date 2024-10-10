from sqlalchemy import Column, String, Enum

from .Base import Base

import enum


class UserRole(enum.Enum):
    LAND_OWNER = "Land Owner"
    BUYER = "Buyer"
    NOTARY = "Notary"
    ADMIN = "Admin"

class User(Base):
    __tablename__ = "users"
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(UserRole))
