#!/usr/bin/env python3

import strawberry
from enum import Enum
from strawberry.directive import DirectiveValue


@strawberry.type
class UserType:
    id: str
    image: str
    name: str
    email: str
    role: str

    @classmethod
    def from_model(cls, user):
        return cls(
            id=str(user.id),
            image=user.image,
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
    image: str
    name: str
    email: str
    user_role: UserRole

@strawberry.input
class UserInput:
    user: UserMetadata

@strawberry.input
class UserUpdateMetadata:
    image: DirectiveValue[str] = None
    name: DirectiveValue[str] = None
    email: DirectiveValue[str] = None
    user_role: DirectiveValue[UserRole] = None

@strawberry.input
class UserUpdateInput:
    user: UserUpdateMetadata