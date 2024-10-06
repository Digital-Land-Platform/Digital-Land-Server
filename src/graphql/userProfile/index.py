from typing import Any, Dict, Optional
from strawberry.scalars import JSON
import strawberry
from strawberry.directive import DirectiveValue
import json
@strawberry.type
class UserProfileType:
    id: DirectiveValue[str] | None
    user_id: DirectiveValue[str] | None
    first_name: DirectiveValue[str] | None
    last_name: DirectiveValue[str] | None
    age: DirectiveValue[int] | None
    gender: DirectiveValue[str] | None
    physical_address: DirectiveValue[str] | None
    identity_card_number: DirectiveValue[str] | None
    whatsapp_number: DirectiveValue[str] | None
    smart_contract: DirectiveValue[str] | None

    @classmethod
    def from_model(cls, user_profile):
        return UserProfileType(
            id=user_profile.id,
            user_id=user_profile.user_id,
            first_name=user_profile.first_name,
            last_name=user_profile.last_name,
            age=user_profile.age,
            gender=user_profile.gender,
            physical_address=user_profile.physical_address,
            identity_card_number=user_profile.identity_card_number,
            whatsapp_number=user_profile.whatsapp_number,
            smart_contract=user_profile.smart_contract
        )

@strawberry.type
class UserProfileAuditLogType:
    id: DirectiveValue[str] | None
    user_profile_id: DirectiveValue[str] | None
    entity: DirectiveValue[str] | None
    action: DirectiveValue[str] | None 
    old_value: DirectiveValue[str] | None
    new_value: JSON| None
    timestamp: DirectiveValue[str] | None

    @classmethod
    def from_model(cls, user_profile_audit_log):
        old_value = user_profile_audit_log.old_value
        new_value = user_profile_audit_log.new_value
        if user_profile_audit_log.old_value:
            old_value= json.loads(user_profile_audit_log.old_value)
        if user_profile_audit_log.new_value:
            new_value = json.loads(user_profile_audit_log.new_value)
        return UserProfileAuditLogType(
            id=str(user_profile_audit_log.id),
            user_profile_id=str(user_profile_audit_log.user_profile_id),
            entity=user_profile_audit_log.entity,
            action=user_profile_audit_log.action.value,
            old_value=old_value,
            new_value=new_value,
            timestamp=user_profile_audit_log.timestamp.isoformat()
        )

@strawberry.input
class UserProfileInput:
    user_id: DirectiveValue[str] = None
    first_name: DirectiveValue[str] = None
    last_name: DirectiveValue[str] = None
    age: DirectiveValue[int] = None
    gender: DirectiveValue[str] = None
    physical_address: DirectiveValue[str] = None
    identity_card_number: DirectiveValue[str] = None
    whatsapp_number: DirectiveValue[str] = None
    smart_contract: DirectiveValue[str] = None