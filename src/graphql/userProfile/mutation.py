from typing import Dict, Optional
import strawberry
from strawberry.directive import DirectiveValue
from .index import UserProfileType, UserProfileInput
from src.models.UserProfile import UserProfile
from fastapi import HTTPException   
from .service import UserProfileService
from src.graphql.users.services import UserService
from src.middleware.UserProfileValidator import UserProfileValidator
from config.database import db

user_service = UserService(db.SessionLocal())
user_profile_service = UserProfileService(db)


@strawberry.type
class UserProfileMutation:

    @strawberry.mutation
    async def create_user_profile(self, user_profile_metadata: UserProfileInput) -> UserProfileType:
        try:
            UserProfileValidator.validate_profile_data(user_profile_metadata)
            if await user_profile_service.check_phone_number(user_profile_metadata.whatsapp_number):
                raise HTTPException(status_code=400, detail="Whatsapp number already exists")
            user = await user_service.get_user_by_id(user_profile_metadata.user_id)
            if not user:
                raise HTTPException(status_code=400, detail="Can not create user profile, User does not exist")
            user_profile_present = await user_profile_service.get_user_profile_by_user_id(user_profile_metadata.user_id)
            if user_profile_present:
                raise HTTPException(status_code=400, detail="User profile already exists")
            user_profile_dict = vars(user_profile_metadata)
            user_profile = UserProfile(**user_profile_dict)
            profile = await user_profile_service.create_user_profile(user_profile)
            if not profile:
                raise HTTPException(status_code=400, detail="Failed to create user profile")
            return UserProfileType.from_model(profile)
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)

    @strawberry.mutation
    async def update_user_profile(self, user_profile_id: DirectiveValue[str], user_profile_metadata: UserProfileInput) -> UserProfileType:
        try:
            user = await user_service.get_user_by_id(user_profile_metadata.user_id)
            if not user:
                raise HTTPException(status_code=400, detail="Can not update user profile, User does not exist")
            user_profile = await user_profile_service.get_user_profile_by_id(user_profile_id)
            if not user_profile:
                raise HTTPException(status_code=400, detail="User profile not found")
            user_profile_dict = vars(user_profile_metadata)
            for key, value in user_profile_dict.items():
                if key == "user_id" and value:
                    validated_value = UserProfileValidator.validate_user_id(value)
                elif key == "first_name" and value:
                    validated_value = UserProfileValidator.validate_name(value, "First name")
                elif key == "last_name" and value:
                    validated_value = UserProfileValidator.validate_name(value, "Last name")
                elif key == "age" and value:
                    validated_value = UserProfileValidator.validate_age(value)
                elif key == "gender" and value:
                    validated_value = UserProfileValidator.validate_gender(value)
                elif key == "physical_address" and value:
                    validated_value = UserProfileValidator.validate_physical_address(value)
                elif key == "identity_card_number" and value:
                    validated_value = UserProfileValidator.validate_identity_card_number(value)
                elif key == "whatsapp_number" and value:
                    validated_value = UserProfileValidator.validate_phone_number(value)
                elif key == "smart_contract" and value:
                    validated_value = UserProfileValidator.validate_smart_contract(value)                
            updated_profile = await user_profile_service.update_user_profile(user_profile_id, user_profile_dict)
            if not updated_profile:
                raise HTTPException(status_code=400, detail="Failed to update user profile")
            return UserProfileType.from_model(updated_profile)
        except HTTPException as e:
            raise strawberry.exceptions.GraphQLError(e.detail)