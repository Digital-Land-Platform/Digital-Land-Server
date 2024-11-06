#!/usr/bin/env python3

import strawberry
from enum import Enum
from strawberry.directive import DirectiveValue


@strawberry.type
class UserType:
    id: str
    image: str
    username: str = None
    email: str
    role: str
    phone_number: DirectiveValue[str] | None
    is_2FA_enabled: bool
    verified: bool
    account_status: str

    @classmethod
    def from_model(cls, user):
        if user.phone_number is None:
            user.phone_number = None
        return cls(
            id=str(user.id),
            image=user.image,
            username=user.username,
            email=user.email,
            role=user.role.value,
            phone_number=user.phone_number,
            is_2FA_enabled=user.is_2FA_enabled,
            verified=user.verified,
            account_status=user.account_status.value
        )

@strawberry.enum
class UserRole(Enum):
    BROKER = "Broker"
    USER = "User"
    NOTARY = "Notary"
    ADMIN = "Admin"

@strawberry.enum
class AccountStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    SUSPENDED = "Suspended"

@strawberry.input
class UserMetadata:
    image: DirectiveValue[str] | None = None
    username: DirectiveValue[str] | None = None
    email: DirectiveValue[str] | None = None
    phone_number: DirectiveValue[str] | None = None
    is_2FA_enabled: DirectiveValue[bool] | None = None
    verified: DirectiveValue[bool] | None = None
    account_status: DirectiveValue[AccountStatus] | None = None
    user_role: DirectiveValue[UserRole] | None = None


@strawberry.input
class UserUpdateMetadata:
    image: DirectiveValue[str] | None = None
    username: DirectiveValue[str] | None = None
    email: DirectiveValue[str] | None = None
    phone_number: DirectiveValue[str] | None = None
    is_2FA_enabled: DirectiveValue[bool] | None = None
    verified: DirectiveValue[bool] | None = None
    account_status: DirectiveValue[AccountStatus] | None = None
    user_role: DirectiveValue[UserRole] | None = None

