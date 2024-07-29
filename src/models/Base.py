from sqlalchemy import UUID, Column, DateTime, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import uuid

BaseModel = declarative_base()


class Base(BaseModel):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
