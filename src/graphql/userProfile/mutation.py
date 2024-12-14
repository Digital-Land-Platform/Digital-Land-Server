from typing import Dict, Optional
import strawberry
from strawberry.directive import DirectiveValue
from .types import UserProfileType, UserProfileInput
from src.models.UserProfile import UserProfile
from fastapi import HTTPException   
from .service import UserProfileService
from src.graphql.users.services import UserService
from src.middleware.UserProfileValidator import UserProfileValidator
from config.database import db
from src.middleware.ErrorHundlers.CustomErrorHandler import ( 
    BadRequestException, CustomException, InternalServerErrorException, NotFoundException 
    )

user_service = UserService(db.SessionLocal())
user_profile_service = UserProfileService(db)


@strawberry.type
class UserProfileMutation:

    @strawberry.mutation
    async def create_user_profile(self, user_profile_metadata: UserProfileInput) -> UserProfileType:
        UserProfileValidator.validate_profile_data(user_profile_metadata)
        
        user = await user_service.get_user_by_id(user_profile_metadata.user_id)
        if not user:
            raise BadRequestException(detail="Can not create user profile, User does not exist")
        
        user_profile_present = await user_profile_service.get_user_profile_by_user_id(user_profile_metadata.user_id)
        if user_profile_present:
            raise CustomException(status_code=409, detail="User profile already exists")
        
        user_profile_dict = vars(user_profile_metadata)
        user_profile_dict["date_of_birth"] = UserProfileValidator.validate_age(user_profile_metadata.date_of_birth)
        user_profile = UserProfile(**user_profile_dict)
        profile = await user_profile_service.create_user_profile(user_profile)
        return UserProfileType.from_model(profile)

    @strawberry.mutation
    async def update_user_profile(self, user_profile_id: DirectiveValue[str], user_profile_metadata: UserProfileInput) -> UserProfileType:

        user = await user_service.get_user_by_id(user_profile_metadata.user_id)
        if not user:
            raise BadRequestException(detail="Can not update user profile, User does not exist")
        
        user_profile = await user_profile_service.get_user_profile_by_id(user_profile_id)
        if not user_profile:
            raise NotFoundException(detail="User profile not found")
        
        user_profile_dict = vars(user_profile_metadata)
        for key, value in user_profile_dict.items():
            if key == "user_id" and value:
                validated_value = UserProfileValidator.validate_id(value)
            elif key == "first_name" and value:
                validated_value = UserProfileValidator.validate_name(value, "First name")
            elif key == "last_name" and value:
                validated_value = UserProfileValidator.validate_name(value, "Last name")
            elif key == "date_of_birth" and value:
                validated_value = UserProfileValidator.validate_age(value)
            elif key == "gender" and value:
                validated_value = UserProfileValidator.validate_gender(value)
            elif key == "license_number" and value:
                validated_value = UserProfileValidator.validate_license_number(value)
            elif key == "location_id" and value:
                validated_value = UserProfileValidator.validate_id(value)

        updated_profile = await user_profile_service.update_user_profile(user_profile_id, user_profile_dict)
        return UserProfileType.from_model(updated_profile)
