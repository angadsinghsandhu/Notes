# ================================================================
# File: hotelmanagement/reservation.py
# Description:
#   Represents a room reservation made by a guest.
#   - Captures reservation details and manages cancellation.
#   - Uses locking to ensure thread-safe updates.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# 7. Exception Handling and Edge Cases.
# ================================================================

from threading import Lock
from datetime import date
from guest import Guest
from room import Room
from reservation_status import ReservationStatus

class Reservation:
    def __init__(self, id: str, guest: Guest, room: Room, check_in_date: date, check_out_date: date):
        self.id = id
        self.guest = guest
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.status = ReservationStatus.CONFIRMED
        self.lock = Lock()

    def cancel(self):
        with self.lock:
            if self.status == ReservationStatus.CONFIRMED:
                self.status = ReservationStatus.CANCELLED
                # Revert room status on cancellation.
                self.room.check_out()
            else:
                raise ValueError("Reservation is not confirmed, cannot cancel.")