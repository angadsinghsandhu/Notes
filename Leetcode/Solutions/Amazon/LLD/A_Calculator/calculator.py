# ================================================================
# File: basic_calculator/calculator.py
# Description:
#   The Calculator class orchestrates arithmetic operations.
#   - It holds a dictionary mapping operation symbols to concrete
#     Operation instances.
#   - Provides a method to calculate results based on the operation.
#
# Steps Covered:
# 4. Determine Core Methods Based on Use Cases.
# 6. Implement Necessary Methods.
# ================================================================

from addition import Addition
from subtraction import Subtraction
from multiplication import Multiplication
from division import Division
from operation import Operation

class Calculator:
    def __init__(self):
        # Register operations with their corresponding symbol.
        self.operations: dict[str, Operation] = {
            '+': Addition(),
            '-': Subtraction(),
            '*': Multiplication(),
            '/': Division()
        }

    def calculate(self, operand1: float, operator: str, operand2: float) -> float:
        if operator not in self.operations:
            raise ValueError(f"Operation '{operator}' is not supported.")
        operation = self.operations[operator]
        result = operation.operate(operand1, operand2)
        return result