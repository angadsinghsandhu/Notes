# ================================================================
# File: basic_calculator/operation.py
# Description:
#   Defines the Operation interface (abstract base class) that all
#   concrete arithmetic operations will implement.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# ================================================================

from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def operate(self, operand1: float, operand2: float) -> float:
        """Perform the operation on two operands and return the result."""
        pass