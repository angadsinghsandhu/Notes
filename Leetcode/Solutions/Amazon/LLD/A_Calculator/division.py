# ================================================================
# File: basic_calculator/division.py
# Description:
#   Implements the Operation interface to perform division.
#   - Handles division by zero by raising an exception.
#
# Steps Covered:
# 4. Determine Core Methods Based on Use Cases.
# 7. Exception Handling and Edge Cases.
# ================================================================

from operation import Operation

class Division(Operation):
    def operate(self, operand1: float, operand2: float) -> float:
        if operand2 == 0:
            raise ValueError("Division by zero is not allowed.")
        return operand1 / operand2