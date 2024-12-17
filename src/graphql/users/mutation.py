#!/usr/bin/env python

from strawberry.directive import DirectiveValue
from fastapi.exceptions import RequestValidationError
import strawberry
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from .services import UserService
from .types import UserType,  UserMetadata, UserUpdateMetadata
from src.models.enums.UserRole import UserRole
from src.models.enums.AccountStatus import AccountStatus
from src.models.User import User
from src.middleware.UserProfileValidator import UserProfileValidator
from fastapi import HTTPException
from config.database import db
from src.middleware.ErrorHundlers.CustomErrorHandler import (
     CustomException, NotFoundException
)
from src.middleware.AuthManagment import AuthManagement

auth_management = AuthManagement()
userService = UserService(db.SessionLocal())

@strawberry.type
class UserMutation:
        
    @strawberry.mutation
    @ExceptionHandler.handle_exceptions
    async def register_user(self, user_input: UserMetadata) -> UserType:
        
        exist_user = await userService.get_user_by_email(user_dict["email"])
        if exist_user:
            raise CustomException(status_code=409, detail="User email already exists")
    
        user_role = UserRole.USER
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

        new_user = User(**user_dict)

        user = await userService.create_user(new_user)
        return UserType.from_model(user)

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def update_user(self, user_id: DirectiveValue[str], user_input: UserUpdateMetadata) -> UserType:
        existing_user = await userService.get_user_by_id(user_id)
        if not existing_user:
            raise NotFoundException("User not found")
        else:
            user_role = UserRole.USER
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
            return UserType.from_model(user)

    @strawberry.mutation
    @auth_management.isAuth()
    @auth_management.role_required([UserRole.ADMIN])
    @ExceptionHandler.handle_exceptions
    async def delete_user(self, user_id:  DirectiveValue[str]) ->  DirectiveValue[str]:
        result = await userService.delete_user(user_id)
        return result
