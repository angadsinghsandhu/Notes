# ================================================================
# File: pizza_ordering/inventory.py
# Description:
#   Manages inventory for pizza ingredients.
#   - Tracks stock levels for each topping and other ingredients.
#   - Provides methods to update inventory when pizzas are ordered.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# 7. Exception Handling and Edge Cases.
# ================================================================

from topping import Topping

class Inventory:
    def __init__(self):
        # Example inventory levels for each topping (could be extended)
        self.stock = {
            Topping.PEPPERONI: 100,
            Topping.MUSHROOMS: 100,
            Topping.ONIONS: 100,
            Topping.SAUSAGE: 100,
            Topping.BACON: 100,
            Topping.EXTRA_CHEESE: 100,
            Topping.BLACK_OLIVES: 100,
            Topping.GREEN_PEPPERS: 100,
            Topping.PINEAPPLE: 100,
            Topping.SPINACH: 100
        }

    def is_available(self, topping: Topping, quantity: int = 1) -> bool:
        # Check if the requested quantity is available.
        return self.stock.get(topping, 0) >= quantity

    def deduct(self, topping: Topping, quantity: int = 1):
        # Deduct a specified quantity from the inventory.
        if self.is_available(topping, quantity):
            self.stock[topping] -= quantity
        else:
            raise ValueError(f"Not enough stock for {topping.value}.")

    def restock(self, topping: Topping, quantity: int):
        # Add stock for the topping.
        if topping in self.stock:
            self.stock[topping] += quantity
        else:
            self.stock[topping] = quantity

    def update_for_order(self, pizzas: list):
        # Deduct ingredients based on the pizzas ordered.
        # For simplicity, assume each topping used in a pizza deducts 1 unit.
        for pizza in pizzas:
            for topping in pizza.toppings:
                self.deduct(topping)