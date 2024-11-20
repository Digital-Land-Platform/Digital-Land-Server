import enum

class AvailabilityStatus(enum.Enum):
    AVAILABLE = "Available"
    BOOKED = "Booked"
    CLOSED = "Closed"