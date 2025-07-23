# ================================================================
# File: hotelmanagement/credit_card_payment.py
# Description:
#   Implements the Payment interface to process credit card payments.
#   - Isolates credit card processing logic, supporting extension or modification later.
#
# Steps Covered:
# 2. Identify Key Entities.
# 4. Determine Core Methods Based on Use Cases.
# 9. Apply Design Patterns (Strategy Pattern via the Payment interface).
# ================================================================

from payment import Payment

class CreditCardPayment(Payment):
    def process_payment(self, amount: float) -> bool:
        # Process credit card payment (assumed to always succeed for this demo)
        # Real implementation would include validation, authorization, etc.
        return True