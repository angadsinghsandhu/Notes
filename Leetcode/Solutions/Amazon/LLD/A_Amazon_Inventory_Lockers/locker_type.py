# ================================================================
# File: locker_type.py
# Description:
#   Defines an enumeration for locker/storage types.
#
# SOLID:
# - SRP: This module is only responsible for representing locker types.
# ================================================================

from enum import Enum

class LockerType(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3