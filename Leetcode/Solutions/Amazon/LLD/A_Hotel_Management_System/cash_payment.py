# ================================================================
# File: hotelmanagement/cash_payment.py
# Description:
#   Implements the Payment interface to process cash payments.
#   - Follows the Single Responsibility Principle by focusing solely on cash processing.
#
# Steps Covered:
# 2. Identify Key Entities.
# 4. Determine Core Methods Based on Use Cases.
# 9. Apply Design Patterns (Strategy Pattern via the Payment interface).
# ================================================================

from payment import Payment

class CashPayment(Payment):
    def process_payment(self, amount: float) -> bool:
        # Process cash payment (assumed to always succeed for this demo)
        # In a real system, additional cash-handling logic would be implemented.
        return True