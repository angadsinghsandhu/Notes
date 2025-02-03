# ================================================================
# File: item.py
# Description:
#   Represents an instance of a product (a package).
#   It contains a unique item ID and a reference to its Product.
#   (An item is the physical instance that will be placed in a locker.)
#
# SOLID:
# - SRP: Only responsible for item-specific details.
# ================================================================

class Item:
    def __init__(self, item_id: str, product):
        self.item_id = item_id
        self.product = product  # Reference to a Product object
        self.locker = None      # The locker where this item is placed

    def set_locker(self, locker):
        self.locker = locker

    def __str__(self):
        return f"Item({self.item_id}, Product: {self.product.name})"