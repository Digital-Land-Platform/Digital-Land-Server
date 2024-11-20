from sqlalchemy import Column, Enum, UUID, ForeignKey, DateTime
from .enums.BookingPlanStatus import BookingPlanStatus
from .Base import Base

class BookingPlan(Base):
    __tablename__ = 'booking_plan'

    natory_id = Column(UUID(as_uuid=True),ForeignKey("users.id"), nullable=False)
    availability_id = Column(UUID(as_uuid=True), ForeignKey('availability.id'), nullable=False, unique=True)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey('transactions.id'), nullable=False, unique=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(BookingPlanStatus), default=BookingPlanStatus.BOOKED)