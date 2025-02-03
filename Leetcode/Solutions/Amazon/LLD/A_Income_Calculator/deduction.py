# ================================================================
# File: income_calculator/deduction.py
# Description:
#   Represents a deduction component.
#   - Encapsulates a deduction amount along with an optional description.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# ================================================================

class Deduction:
    def __init__(self, amount: float, description: str = ""):
        self.amount = amount
        self.description = description