"""Create and keep in-memory room bookings.

A BookingService instance holds its own bookings until the Python process ends.
Times are whole minutes after midnight (0 through 1440). Each booking is a
half-open interval: the start is included and the end is excluded.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Booking:
    room: str
    start: int
    end: int
    guest: str


class BookingService:
    def __init__(self) -> None:
        self._bookings: list[Booking] = []

    def create_booking(self, room: str, start: int, end: int, guest: str) -> Booking:
        """Create one booking, or raise ValueError for invalid input."""
        if not room.strip():
            raise ValueError("room must not be blank")
        if not guest.strip():
            raise ValueError("guest must not be blank")
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError("start and end must be whole minutes")
        if not (0 <= start < end <= 1440):
            raise ValueError("time must satisfy 0 <= start < end <= 1440")

        for existing in self._bookings:
            if existing.room != room:
                continue
            if existing.start < end and start < existing.end:
                raise ValueError("booking overlaps an existing booking in the same room")

        booking = Booking(room=room, start=start, end=end, guest=guest)
        self._bookings.append(booking)
        return booking

    def list_bookings(self) -> tuple[Booking, ...]:
        """Return a read-only snapshot in creation order."""
        return tuple(self._bookings)
