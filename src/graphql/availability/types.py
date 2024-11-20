import strawberry
import enum

@strawberry.enum
class AvailabilityEnum(enum.Enum):
    AVAILABLE = "Available"
    BOOKED = "Booked"
    CLOSED = "Closed"

@strawberry.type
class AvailabilityType:
    id: str
    natory_id: str
    start_time: str
    end_time: str
    status: AvailabilityEnum | None = None

    @classmethod
    def from_orm(cls, availability):
        status_ = None
        if availability.status:
            try:
                # Map AvailabilityStatus to AvailabilityEnum
                status_ = AvailabilityEnum[availability.status.name]
            except KeyError:
                raise ValueError(f"Invalid status: {availability.status}")
        return cls(
            id=availability.id,
            natory_id=availability.natory_id,
            start_time=availability.start_time,
            end_time=availability.end_time,
            status=status_
        )

@strawberry.input
class AvailabilityInput:
    natory_id: str
    start_time: str
    end_time: str
    status: AvailabilityEnum | None = None

@strawberry.input
class UpdateAvailabiltyInput:
    notation_id: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    status: AvailabilityEnum | None = None
@strawberry.input
class ChooseAvailabilityInput:
    status: AvailabilityEnum