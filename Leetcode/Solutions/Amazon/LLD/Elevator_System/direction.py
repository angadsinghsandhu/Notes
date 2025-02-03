# ================================================================
# File: elevatorsystem/direction.py
# Description:
#   Defines the Direction enum which represents the possible movement 
#   directions for an elevator (UP or DOWN).
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Enumerations.
# ================================================================

from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2