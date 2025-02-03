# ================================================================
# File: transaction_value_rule.py
# Description:
#   Implements a Transaction Value Rule.
#   Checks if the transaction value meets a minimum threshold.
#
# Steps Covered:
# 4. Determine Core Methods Based on Use Cases.
# ================================================================

from rule import Rule
from rule_types import RuleTypes

class TransactionValueRule(Rule):
    def __init__(self, name: str, min_value: float):
        super().__init__(name, RuleTypes.TRANSACTION_VALUE_LIMIT)
        self.__min_value = min_value

    def can_apply(self, user, transaction, coupon) -> bool:
        # Assume transaction has a method get_cart_value()
        if transaction.get_cart_value() >= self.__min_value:
            return True
        return False