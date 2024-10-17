#!/usr/bin/env python3

import strawberry
from enum import Enum


@strawberry.type
class UserType:
    id: str
    name: str
    email: str
    role: str

    @classmethod
    def from_model(cls, user):
        return cls(
            id=str(user.id),
            name=user.name,
            email=user.email,
            role=user.role.value
        )

@strawberry.enum
class UserRole(Enum):
    LAND_OWNER = "Land Owner"
    BUYER = "Buyer"
    NOTARY = "Notary"
    ADMIN = "Admin"

@strawberry.input
class UserMetadata:
    name: str
    email: str
    user_role: UserRole

@strawberry.input
class UserInput:
    user: UserMetadata