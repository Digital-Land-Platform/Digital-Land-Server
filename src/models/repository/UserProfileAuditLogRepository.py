from datetime import datetime
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List
import json
from src.models.UserProfileAuditLog import UserProfileAuditLog

class UserProfileAuditLogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_audit_log(self, log_file: Dict) -> UserProfileAuditLog:
        try:
            print("Log file before: ", log_file)
            async with self.db as session:
                for key in ["new_value", "old_value"]:
                    if key in log_file and log_file[key]:
                        # Remove non-serializable fields
                        log_file[key].pop('_sa_instance_state', None)
                        log_file[key].pop('user_profile', None)
                        # Convert UUID and datetime objects to strings
                        log_file[key] = json.dumps({
                    k: (str(v) if isinstance(v, uuid.UUID) else v.isoformat() if isinstance(v, datetime) else v)
                    for k, v in log_file[key].items()
                })
                audit_log = UserProfileAuditLog(**log_file)
                session.add(audit_log)
                await session.commit()
                await session.refresh(audit_log)
                return audit_log
        except SQLAlchemyError as e:
            raise Exception(f"Failed to create audit log: {e}")
        
    async def get_audit_logs(self, user_profile_id: uuid.UUID) -> List[UserProfileAuditLog]:
        try:
            async with self.db as session:
                statement = select(UserProfileAuditLog).where(UserProfileAuditLog.user_profile_id == user_profile_id)
                query = await session.execute(statement)
                return query.scalars().all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get audit logs: {e}")
