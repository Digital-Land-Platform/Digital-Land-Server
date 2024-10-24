#!/usr/bin/env python

from strawberry.directive import DirectiveValue
from fastapi.exceptions import RequestValidationError
import strawberry
from .services import UserService
from .types import UserType,  UserMetadata, UserUpdateMetadata
from src.models.enums.UserRole import UserRole
from src.models.enums.AccountStatus import AccountStatus
from src.models.User import User
from src.middleware.UserProfileValidator import UserProfileValidator
from fastapi import HTTPException
from config.database import db

userService = UserService(db.SessionLocal())

@strawberry.type
class UserMutation:
        
    @strawberry.mutation
    async def register_user(self, user_input: UserMetadata) -> UserType:
        try:
            user_role = UserRole.ADMIN
            if user_input.user_role.value == UserRole.USER.value:
                user_role = UserRole.USER
            elif user_input.user_role.value == UserRole.NOTARY.value:
                user_role = UserRole.NOTARY
            elif user_input.user_role.value == UserRole.BROKER.value:
                user_role = UserRole.BROKER
            account_status = AccountStatus.INACTIVE
            if user_input.account_status.value == AccountStatus.ACTIVE.value:
                account_status = AccountStatus.ACTIVE
            elif user_input.account_status.value == AccountStatus.SUSPENDED.value:
                account_status = AccountStatus.SUSPENDED
            UserProfileValidator.validate_name(user_input.username, "username")
            UserProfileValidator.validate_phone_number(user_input.phone_number)

            user_dict = {
                "image": user_input.image,
                "username": user_input.username,
                "email": user_input.email,
                "phone_number": user_input.phone_number,
                "is_2FA_enabled": user_input.is_2FA_enabled,
                "verified": user_input.verified,
                "account_status": account_status,
                "role": user_role
            }
            exist_user = await userService.get_user_by_email(user_dict["email"])
            if exist_user:
                raise HTTPException(status_code=400, detail="User email already exists")
            print("User dict: ", user_dict)
            new_user = User(**user_dict)
            user = await userService.create_user(new_user)
            if not user:
                raise HTTPException(status_code=400, detail="Failed to create user")
            return UserType.from_model(user)
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)
        except RequestValidationError as e:
            raise strawberry.exceptions.GraphQLError(str(e))

    @strawberry.mutation
    async def update_user(self, user_id: DirectiveValue[str], user_input: UserUpdateMetadata) -> UserType:
        try:
            user_role = UserRole.ADMIN
            if user_input.user_role:
                if user_input.user_role.value == UserRole.USER.value:
                    user_role = UserRole.USER
                elif user_input.user_role.value == UserRole.NOTARY.value:
                    user_role = UserRole.NOTARY
                elif user_input.user_role.value == UserRole.BROKER.value:
                    user_role = UserRole.BROKER
            account_status = AccountStatus.INACTIVE
            if user_input.account_status:
                if user_input.account_status.value == AccountStatus.ACTIVE.value:
                    account_status = AccountStatus.ACTIVE
                elif user_input.account_status.value == AccountStatus.SUSPENDED.value:
                    account_status = AccountStatus.SUSPENDED
                
            user_dict = {
                "image": user_input.image,
                "username": user_input.username,
                "email": user_input.email,
                "phone_number": user_input.phone_number,
                "is_2FA_enabled": user_input.is_2FA_enabled,
                "verified": user_input.verified,
                "account_status": account_status,
                "role": user_role
            } 
            user = await userService.update_user(user_id, user_dict)
            if not user:
                raise HTTPException(status_code=400, detail="Failed to update user")
            return UserType.from_model(user)
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)
        except RequestValidationError as e:
            raise strawberry.exceptions.GraphQLError(str(e))

    @strawberry.mutation
    async def delete_user(self, user_id:  DirectiveValue[str]) ->  DirectiveValue[str]:
        try:
            result = await userService.delete_user(user_id)
            return result
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)
        except RequestValidationError as e:
            raise strawberry.exceptions.GraphQLError(str(e))