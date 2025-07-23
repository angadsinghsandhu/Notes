# ================================================================
# File: hotelmanagement/room_status.py
# Description:
#   Enumerates the possible statuses for a hotel room.
#   - Manages room availability and booking lifecycle.
#
# Steps Covered:
# 2. Identify Key Entities.
# ================================================================

from enum import Enum

class RoomStatus(Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"
    OCCUPIED = "OCCUPIED"