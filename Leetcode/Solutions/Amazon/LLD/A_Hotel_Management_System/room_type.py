# ================================================================
# File: hotelmanagement/room_type.py
# Description:
#   Enumerates different types of hotel rooms.
#   - Allows the system to handle multiple room types.
#
# Steps Covered:
# 2. Identify Key Entities.
# ================================================================

from enum import Enum

class RoomType(Enum):
    SINGLE = "SINGLE"
    DOUBLE = "DOUBLE"
    DELUXE = "DELUXE"
    SUITE = "SUITE"