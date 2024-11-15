import strawberry
import enum

@strawberry.enum
class BookingPlanEnum(enum.Enum):
    BOOKED = "Booked"
    COMPLETED = "Completed"
    CLOSED = "Closed"

@strawberry.type
class BookingPlanType:
    id: str
    natory_id: str
    availability_id: str
    transaction_id: str
    start_time: str
    end_time: str
    status: BookingPlanEnum | None = None

    @classmethod
    def from_orm(cls, booking_plan):
        status_ = None
        if booking_plan.status:
            try:
                # Map BookingPlanStatus to BookingPlanEnum
                status_ = BookingPlanEnum[booking_plan.status.name]
            except KeyError:
                raise ValueError(f"Invalid status: {booking_plan.status}")
        return cls(
            id=booking_plan.id,
            natory_id=booking_plan.natory_id,
            availability_id=booking_plan.availability_id,
            transaction_id=booking_plan.transaction_id,
            start_time=booking_plan.start_time,
            end_time=booking_plan.end_time,
            status=status_
        )

@strawberry.input
class BookingPlanInput:
    natory_id: str | None = None
    availability_id: str
    transaction_id: str
    start_time: str | None = None
    end_time: str | None = None
    status: BookingPlanEnum | None = None

@strawberry.input
class ChooseBookingPlanInput:
    status: BookingPlanEnum

@strawberry.input
class UpdateBookingPlanInput:
    natory_id: str | None = None
    availability_id: str | None = None
    transaction_id: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    status: BookingPlanEnum | None = None