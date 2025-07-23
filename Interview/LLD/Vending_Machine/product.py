# ================================================================
# File: vendingmachine/product.py
# Description:
#   Represents a product in the vending machine.
#   - Holds the product name and price.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# ================================================================

class Product:
    def __init__(self, name, price):
        self.name = name    # Name of the product.
        self.price = price  # Price of the product.