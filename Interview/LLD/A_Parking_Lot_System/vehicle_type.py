# ================================================================
# File: parkinglot/vehicle_type.py
# Description:
#   Enumerates different types of vehicles.
#   - Acts as a simple type system to distinguish vehicle sizes.
#
# Steps Covered:
# 2. Identify Key Entities.
# ================================================================

from enum import Enum

class VehicleType(Enum):
    CAR = 1
    MOTORCYCLE = 2
    TRUCK = 3
