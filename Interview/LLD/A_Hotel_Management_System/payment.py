# ================================================================
# File: hotelmanagement/payment.py
# Description:
#   Abstract Payment class that defines a contract for processing payments.
#   - This allows multiple payment strategies (e.g., cash, credit card).
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 9. Apply Design Patterns (Strategy Pattern).
# ================================================================

from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Process the payment of a given amount and return True if successful."""
        pass