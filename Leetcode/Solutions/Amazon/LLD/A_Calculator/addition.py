# ================================================================
# File: basic_calculator/addition.py
# Description:
#   Implements the Operation interface to perform addition.
#
# Steps Covered:
# 4. Determine Core Methods Based on Use Cases.
# ================================================================

from operation import Operation

class Addition(Operation):
    def operate(self, operand1: float, operand2: float) -> float:
        return operand1 + operand2