# ================================================================
# File: vendingmachine/note.py
# Description:
#   Defines the Note enum with supported note denominations.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# ================================================================

from enum import Enum

class Note(Enum):
    ONE = 1
    FIVE = 5
    TEN = 10
    TWENTY = 20