# ================================================================
# File: hotelmanagement/reservation_status.py
# Description:
#   Enumerates the possible statuses for a reservation.
#   - Supports the reservation lifecycle (confirmed, cancelled).
#
# Steps Covered:
# 2. Identify Key Entities.
# ================================================================

from enum import Enum

class ReservationStatus(Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"