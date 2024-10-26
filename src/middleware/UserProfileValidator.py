# src/utils/profile_validator.py

import re
import uuid
import phonenumbers
from phonenumbers import NumberParseException
from typing import Dict, Any

class UserProfileValidator:
    
    @staticmethod
    def validate_user_id(user_id: Any) -> uuid.UUID:
        if not isinstance(user_id, uuid.UUID):
            try:
                user_id = uuid.UUID(user_id)
            except ValueError:
                raise ValueError("Invalid user ID format.")
        return user_id

    @staticmethod
    def validate_name(name: str, field_name: str) -> str:
        if not (1 <= len(name.strip()) <= 50) or not name.isalpha():
            raise ValueError(f"{field_name} must contain only alphabetic characters and be between 1 and 50 characters.")
        return name.strip()

    @staticmethod
    def validate_age(age: int) -> int:
        if not (18 <= age <= 120):
            raise ValueError("Age must be between 0 and 120.")
        return age

    @staticmethod
    def validate_gender(gender: str) -> str:
        if gender not in {"Male", "Female"}:
            raise ValueError("Gender must be 'Male', 'Female'.")
        return gender

    @staticmethod
    def validate_physical_address(address: str) -> str:
        if len(address.strip()) > 255:
            raise ValueError("Physical address is very long.")
        return address.strip()

    @staticmethod
    def validate_identity_card_number(identity_card_number: str) -> str:
        if not re.fullmatch(r"^\d{16}$", identity_card_number):
            raise ValueError("Identity card number must be a 16-digit number.")
        return identity_card_number

    @staticmethod
    def validate_phone_number(phone_number: str) -> str:
        try:
            # Parse the phone number without specifying the country code
            parsed_number = phonenumbers.parse(phone_number, None)
            
            # Check if the number is valid and possible
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("Invalid phone number.")
            
            # Convert the phone number to the international format
            international_number = phonenumbers.format_number(
                parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
            
            return international_number
        except NumberParseException:
            raise ValueError("Phone number is not in a valid international format.")

    @staticmethod
    def validate_smart_contract(smart_contract: str) -> str:
        if not smart_contract:
            raise ValueError("Smart contract cannot be empty.")
        return smart_contract

    @staticmethod
    def validate_profile_data(data: Dict[str, Any]) -> Dict[str, Any]:
        validated_data = {}
        validated_data["user_id"] = UserProfileValidator.validate_user_id(data.user_id)
        validated_data["first_name"] = UserProfileValidator.validate_name(data.first_name, "First name")
        validated_data["last_name"] = UserProfileValidator.validate_name(data.last_name, "Last name")
        validated_data["age"] = UserProfileValidator.validate_age(data.age)
        validated_data["gender"] = UserProfileValidator.validate_gender(data.gender)
        validated_data["physical_address"] = UserProfileValidator.validate_physical_address(data.physical_address)
        validated_data["identity_card_number"] = UserProfileValidator.validate_identity_card_number(data.identity_card_number)
        validated_data["whatsapp_number"] = UserProfileValidator.validate_phone_number(data.whatsapp_number)
        validated_data["smart_contract"] = UserProfileValidator.validate_smart_contract(data.smart_contract)
        return validated_data
