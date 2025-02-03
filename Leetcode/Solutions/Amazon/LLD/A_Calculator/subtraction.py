# ================================================================
# File: basic_calculator/subtraction.py
# Description:
#   Implements the Operation interface to perform subtraction.
#
# Steps Covered:
# 4. Determine Core Methods Based on Use Cases.
# ================================================================

from operation import Operation

class Subtraction(Operation):
    def operate(self, operand1: float, operand2: float) -> float:
        return operand1 - operand2