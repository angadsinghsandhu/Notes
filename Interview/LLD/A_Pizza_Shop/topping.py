# ================================================================
# File: pizza_ordering/topping.py
# Description:
#   Defines the available toppings for pizzas.
#   - This enumeration represents various topping options.
#
# Steps Covered:
# 2. Identify Key Entities.
# ================================================================

from enum import Enum

class Topping(Enum):
    PEPPERONI = "Pepperoni"
    MUSHROOMS = "Mushrooms"
    ONIONS = "Onions"
    SAUSAGE = "Sausage"
    BACON = "Bacon"
    EXTRA_CHEESE = "Extra Cheese"
    BLACK_OLIVES = "Black Olives"
    GREEN_PEPPERS = "Green Peppers"
    PINEAPPLE = "Pineapple"
    SPINACH = "Spinach"