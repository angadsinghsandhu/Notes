# ================================================================
# File: income_calculator/bonus.py
# Description:
#   Represents a bonus component.
#   - Encapsulates a bonus amount along with an optional description.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# ================================================================

class Bonus:
    def __init__(self, amount: float, description: str = ""):
        self.amount = amount
        self.description = description