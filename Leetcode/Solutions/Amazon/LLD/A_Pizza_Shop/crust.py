# ================================================================
# File: pizza_ordering/crust.py
# Description:
#   Defines the available types of pizza crusts.
#   - This is an enumeration that allows easy extension if new crust types are added.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# ================================================================

from enum import Enum

class Crust(Enum):
    THIN = "Thin Crust"
    THICK = "Thick Crust"
    STUFFED = "Stuffed Crust"