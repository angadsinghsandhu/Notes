# ================================================================
# File: age_limit_rule.py
# Description:
#   Implements an Age Limit Rule.
#   Checks if the user’s age falls within a specified range.
#
# Steps Covered:
# 4. Determine Core Methods Based on Use Cases.
# ================================================================

from rule import Rule
from rule_types import RuleTypes

class AgeLimitRule(Rule):
    def __init__(self, name: str, initial_age: int, final_age: int = None):
        super().__init__(name, RuleTypes.AGE_LIMIT)
        self.__initial_age = initial_age
        # If no final_age is provided, assume no upper limit.
        self.__final_age = final_age if final_age is not None else float('inf')

    def can_apply(self, user, transaction, coupon) -> bool:
        user_age = user.get_age()  # Assume user has a get_age() method.
        if user_age is not None and self.__initial_age <= user_age <= self.__final_age:
            return True
        return False