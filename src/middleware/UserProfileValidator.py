# src/utils/profile_validator.py

from datetime import date, datetime
import re
import uuid
import phonenumbers
from phonenumbers import NumberParseException
from typing import Dict, Any

class UserProfileValidator:
    
    @staticmethod
    def validate_id(id: Any) -> uuid.UUID:
        if not isinstance(id, uuid.UUID):
            try:
                user_id = uuid.UUID(id)
            except ValueError:
                raise ValueError("Invalid user ID format.")
        return user_id

    @staticmethod
    def validate_name(name: str, field_name: str) -> str:
        if not (1 <= len(name.strip()) <= 50) or not name.isalpha():
            raise ValueError(f"{field_name} must contain only alphabetic characters and be between 1 and 50 characters.")
        return name.strip()

    @staticmethod
    def validate_age(dob: str) -> date:
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d").date()  # Adjust the format as needed
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        
        today = date.today()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        
        if not (18 <= age <= 120):
            raise ValueError("Age must be between 18 and 120.")
        
        return dob_date

    @staticmethod
    def validate_gender(gender: str) -> str:
        if gender not in {"Male", "Female", "Other"}:
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
    def change_str_date(date_str: str, value: str=None) -> date:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Invalid date format {value}. Use YYYY-MM-DD or YYYY-MM-DD H:M:S.")
        except Exception as e:
            raise ValueError(f"Invalid date format {value}. {e}")
        

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
    def validate_license_number(license_number: str) -> str:
        if not license_number or len(license_number) > 30:
            raise ValueError("License number must not be empty and should be at most 30 characters.")
        return license_number.strip()

    @staticmethod
    def validate_profile_data(data: Dict[str, Any]) -> Dict[str, Any]:
        validated_data = {}
        validated_data["user_id"] = UserProfileValidator.validate_id(data.user_id)
        validated_data["first_name"] = UserProfileValidator.validate_name(data.first_name, "First name")
        validated_data["last_name"] = UserProfileValidator.validate_name(data.last_name, "Last name")
        validated_data["date_of_birth"] = UserProfileValidator.validate_age(data.date_of_birth)
        validated_data["gender"] = UserProfileValidator.validate_gender(data.gender)
        validated_data["location_id"] = UserProfileValidator.validate_id(data.location_id)
        validated_data["date_of_birth"] = UserProfileValidator.validate_age(data.date_of_birth)
        validated_data["license_number"] = UserProfileValidator.validate_license_number(data.license_number)
        return validated_data
