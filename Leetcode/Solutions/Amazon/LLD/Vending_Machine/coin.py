# ================================================================
# File: vendingmachine/coin.py
# Description:
#   Defines the Coin enum with supported coin denominations.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# ================================================================

from enum import Enum

class Coin(Enum):
    PENNY = 0.01
    NICKEL = 0.05
    DIME = 0.1
    QUARTER = 0.25