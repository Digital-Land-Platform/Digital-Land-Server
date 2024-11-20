import enum

class BookingPlanStatus(enum.Enum):
    BOOKED = "Booked"
    COMPLETED = "Completed"
    CLOSED = "Closed"