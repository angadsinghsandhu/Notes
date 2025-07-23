# ================================================================
# File: coupon.py
# Description:
#   Coupon is a type of Token with additional rules and utilization tracking.
#   Coupons can have overall use limits and per-user limits.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# ================================================================

from token import Token
from promotion_status import PromotionStatus

class Coupon(Token):
    def __init__(self, coupon_id: int, expiry_duration_in_days: int, name: str, description: str, creator: str, 
                 status: PromotionStatus, rules: list):
        super().__init__(expiry_duration_in_days, name, description, creator, status)
        self.__coupon_id = coupon_id
        self.__rules = rules  # List of rule objects that validate coupon application.
        # Utilization mapping: {user_id: usage_count} for per-user tracking.
        self.utilization = {}

    def add_rule(self, rule):
        self.__rules.append(rule)

    def can_apply_coupon(self, user, transaction) -> bool:
        # Evaluate each rule; if any rule fails, the coupon cannot be applied.
        for rule in self.__rules:
            if not rule.can_apply(user, transaction, self):
                return False
        return True