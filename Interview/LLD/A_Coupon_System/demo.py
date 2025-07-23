# ================================================================
# File: coupon_voucher_demo.py
# Description:
#   Demonstrates usage of the coupon and voucher management system.
#   - Admin creates coupons and vouchers.
#   - User views and applies promotions.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 6. Implement Necessary Methods.
# 8. Follow Good Coding Practices.
# ================================================================

from system import System
from coupon import Coupon
from voucher import Voucher
from promotion_status import PromotionStatus
from age_limit_rule import AgeLimitRule
from transaction_value_rule import TransactionValueRule
from admin import Admin
from user import User
from account import Account

def main():
    # Initialize the system (Singleton).
    system = System.get_instance()

    # Create an admin.
    admin_account = Account("admin@example.com", "adminpass")
    admin = Admin("AdminUser", 35, admin_account)

    # Create rules.
    age_rule = AgeLimitRule("Age Rule", 18, 60)
    txn_rule = TransactionValueRule("Cart Value Rule", 1000)

    # Create a coupon with two rules.
    coupon = Coupon(coupon_id=101, expiry_duration_in_days=30, name="SAVE20", 
                    description="20% off on orders above 1000", creator="AdminUser",
                    status=PromotionStatus.ACTIVE, rules=[age_rule, txn_rule])
    admin.create_coupon(coupon)

    # Create an unassigned voucher.
    voucher = Voucher(expiry_duration_in_days=15, name="WELCOME", 
                      description="Welcome offer voucher", creator="AdminUser",
                      status=PromotionStatus.ACTIVE, user=None)
    admin.create_voucher(voucher)

    # Create a user.
    user_account = Account("user@example.com", "userpass")
    user = User("RegularUser", 25, user_account)

    # Assume we have a transaction object with a get_cart_value() method.
    # For demonstration, we create a dummy transaction with an attribute.
    class Transaction:
        def __init__(self, cart_value):
            self.cart_value = cart_value
        def get_cart_value(self):
            return self.cart_value

    transaction = Transaction(cart_value=1200)

    # User views available promotions.
    available_promos = user.get_available_promotions(transaction)
    print(f"User {user.get_name()} sees {len(available_promos)} available promotions.")

    # User applies a promotion (coupon/voucher) by code.
    if user.apply_promotion("SAVE20", transaction):
        print("Promotion applied successfully!")
    else:
        print("Promotion could not be applied.")

if __name__ == "__main__":
    main()