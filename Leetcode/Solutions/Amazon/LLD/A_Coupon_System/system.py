# ================================================================
# File: system.py
# Description:
#   Implements a Singleton System class to store and manage coupons and vouchers.
#   Provides APIs to add, update, delete, and retrieve promotions.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# 7. Concurrency / Thread Safety can be added as needed.
# ================================================================

from coupon import Coupon
from voucher import Voucher

class System:
    __instance = None

    def __init__(self):
        if System.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.__coupons = {}   # coupon_id -> Coupon object.
            self.__vouchers = {}  # voucher_id -> Voucher object.
            System.__instance = self

    @staticmethod
    def get_instance():
        if System.__instance is None:
            System()
        return System.__instance

    def add_coupon(self, coupon: Coupon):
        self.__coupons[coupon._Coupon__coupon_id] = coupon

    def update_coupon(self, coupon: Coupon):
        self.__coupons[coupon._Coupon__coupon_id] = coupon

    def delete_coupon(self, coupon_id: int):
        if coupon_id in self.__coupons:
            del self.__coupons[coupon_id]

    def add_voucher(self, voucher: Voucher):
        # Assume voucher has an attribute "id" (omitted for brevity)
        self.__vouchers[voucher._Voucher__user] = voucher

    def update_voucher(self, voucher: Voucher):
        self.__vouchers[voucher._Voucher__user] = voucher

    def delete_voucher(self, voucher_id):
        if voucher_id in self.__vouchers:
            del self.__vouchers[voucher_id]

    def get_active_coupons(self, user, transaction):
        # Return a list of coupons that are active and pass rule validations.
        result = []
        for coupon in self.__coupons.values():
            if coupon._Token__status.name == "ACTIVE" and not coupon.is_expired():
                if coupon.can_apply_coupon(user, transaction):
                    result.append(coupon)
        return result

    def get_available_vouchers(self, user):
        # Return vouchers that are either unassigned or assigned to the user.
        result = []
        for voucher in self.__vouchers.values():
            if voucher._Token__status.name == "ACTIVE" and not voucher.is_expired():
                # For simplicity, assume if voucher.__user is None or equals user id.
                result.append(voucher)
        return result

    def apply_promotion(self, user, transaction, promotion_code: str) -> bool:
        # Find the promotion by code (code lookup omitted for brevity) and validate.
        # For example, first try coupons then vouchers.
        # Return True if applied, False otherwise.
        # (Detailed implementation is omitted for brevity.)
        return True