# ================================================================
# File: user.py
# Description:
#   Represents a regular user who can view and apply promotions.
#
# Steps Covered:
# 2. Identify Key Entities.
# ================================================================

from account import Account
from person import Person  # See next file.
from system import System

class User(Person):
    def __init__(self, name: str, age: int, account: Account):
        super().__init__(name, age)
        self.__account = account
        self.system = System.get_instance()

    def get_available_promotions(self, transaction):
        # Retrieve all active coupons and vouchers valid for this user/transaction.
        coupons = self.system.get_active_coupons(self, transaction)
        vouchers = self.system.get_available_vouchers(self)
        return coupons + vouchers

    def apply_promotion(self, promotion_code: str, transaction) -> bool:
        return self.system.apply_promotion(self, transaction, promotion_code)