# ================================================================
# File: pizza_ordering/pizza.py
# Description:
#   The Pizza class represents a customizable pizza.
#   - It allows setting the size, crust type, and adding multiple toppings.
#   - It provides methods to calculate the price based on customizations.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# ================================================================

from crust import Crust
from topping import Topping

class Pizza:
    def __init__(self, size: str, crust: Crust):
        """
        size: e.g., "Small", "Medium", "Large"
        crust: an instance of Crust enum
        """
        self.size = size
        self.crust = crust
        self.toppings = []  # List of Topping enums

    def add_topping(self, topping: Topping):
        # Allows customers to customize their pizza with additional toppings.
        self.toppings.append(topping)

    def remove_topping(self, topping: Topping):
        if topping in self.toppings:
            self.toppings.remove(topping)

    def calculate_price(self) -> float:
        # Base prices for different sizes (could be extended or externalized)
        base_prices = {"Small": 8.0, "Medium": 10.0, "Large": 12.0}
        # Additional costs
        crust_cost = {
            Crust.THIN: 0.0,
            Crust.THICK: 1.0,
            Crust.STUFFED: 2.0
        }
        topping_cost = 0.5 * len(self.toppings)

        price = base_prices.get(self.size, 10.0) + crust_cost[self.crust] + topping_cost
        return price

    def __str__(self):
        toppings_str = ", ".join([t.value for t in self.toppings]) if self.toppings else "No toppings"
        return f"{self.size} pizza with {self.crust.value} and toppings: {toppings_str}"