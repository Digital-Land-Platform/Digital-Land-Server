from sqlalchemy import Column, Enum, UUID, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .enums.AvailabityStatus import AvailabilityStatus
from .Base import Base
from .BookingPlan import BookingPlan

class Availability(Base):
    __tablename__ = 'availability'

    natory_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(AvailabilityStatus), default=AvailabilityStatus.AVAILABLE)

    BookingPlan = relationship("BookingPlan", backref="availability", cascade="all, delete, delete-orphan")
    