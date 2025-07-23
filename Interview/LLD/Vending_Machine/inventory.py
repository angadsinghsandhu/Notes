# ================================================================
# File: vendingmachine/inventory.py
# Description:
#   Manages the available products and their quantities.
#   - Uses a dictionary (could be extended to a thread-safe data structure) for product management.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 7. Exception Handling / Edge Cases.
# ================================================================

class Inventory:
    def __init__(self):
        self.products = {}  # Maps Product to its available quantity.

    def add_product(self, product, quantity):
        self.products[product] = quantity

    def remove_product(self, product):
        if product in self.products:
            del self.products[product]

    def update_quantity(self, product, quantity):
        self.products[product] = quantity

    def get_quantity(self, product):
        return self.products.get(product, 0)

    def is_available(self, product):
        return product in self.products and self.products[product] > 0