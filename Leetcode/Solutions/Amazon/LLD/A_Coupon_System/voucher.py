# ================================================================
# File: voucher.py
# Description:
#   Voucher is a type of Token. It is further categorized as:
#     - Unassigned: Any user can use it (one-time use).
#     - PreAssigned: Tied to a specific user.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# ================================================================

from token import Token
from promotion_status import PromotionStatus

class Voucher(Token):
    def __init__(self, expiry_duration_in_days: int, name: str, description: str, creator: str, 
                 status: PromotionStatus = PromotionStatus.ACTIVE, user: str = None):
        super().__init__(expiry_duration_in_days, name, description, creator, status)
        self.__user = user  # If None, then voucher is unassigned.
        self.__is_used = False

    def mark_used(self):
        self.__is_used = True

    def is_used(self) -> bool:
        return self.__is_used