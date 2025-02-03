# ================================================================
# File: admin.py
# Description:
#   Represents an Admin who can create, update, and delete coupons and vouchers.
#   Uses the PromotionService to perform operations.
#
# Steps Covered:
# 2. Identify Key Entities.
# 4. Determine Core Methods Based on Use Cases.
# ================================================================

from account import Account
from person import Person  # See next file.
from system import System  # Our central repository (Singleton)

class Admin(Person):
    def __init__(self, name: str, age: int, account: Account):
        super().__init__(name, age)
        self.__account = account
        # Assume the System singleton holds the promotion data.
        self.system = System.get_instance()

    def create_coupon(self, coupon):
        # Delegate coupon creation to the system or a dedicated service.
        self.system.add_coupon(coupon)

    def update_coupon(self, coupon):
        self.system.update_coupon(coupon)

    def delete_coupon(self, coupon_id: int):
        self.system.delete_coupon(coupon_id)

    def create_voucher(self, voucher):
        self.system.add_voucher(voucher)

    def update_voucher(self, voucher):
        self.system.update_voucher(voucher)

    def delete_voucher(self, voucher_id: int):
        self.system.delete_voucher(voucher_id)