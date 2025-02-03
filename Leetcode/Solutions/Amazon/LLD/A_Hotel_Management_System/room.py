# ================================================================
# File: hotelmanagement/room.py
# Description:
#   Represents a hotel room.
#   - Manages room details (id, type, price) and status.
#   - Handles room state transitions (booking, check-in, check-out) with proper locking for thread-safety.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# 7. Exception Handling and Edge Cases.
# ================================================================

from threading import Lock
from room_status import RoomStatus
from room_type import RoomType

class Room:
    def __init__(self, id: str, type: RoomType, price: float):
        self.id = id
        self.type = type
        self.price = price
        self.status = RoomStatus.AVAILABLE
        self.lock = Lock()

    def book(self):
        with self.lock:
            if self.status == RoomStatus.AVAILABLE:
                self.status = RoomStatus.BOOKED
            else:
                raise ValueError("Room is not available for booking.")

    def check_in(self):
        with self.lock:
            if self.status == RoomStatus.BOOKED:
                self.status = RoomStatus.OCCUPIED
            else:
                raise ValueError("Room is not booked, cannot check in.")

    def check_out(self):
        with self.lock:
            if self.status == RoomStatus.OCCUPIED:
                self.status = RoomStatus.AVAILABLE
            else:
                raise ValueError("Room is not occupied, cannot check out.")