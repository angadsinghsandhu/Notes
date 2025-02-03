# ================================================================
# File: pizza_ordering/order.py
# Description:
#   Represents a pizza order.
#   - An order can include one or more pizzas.
#   - Manages the order status and calculates the total price.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# ================================================================

import uuid
from order_status import OrderStatus
from pizza import Pizza

class Order:
    def __init__(self):
        self.id = self._generate_order_id()
        self.pizzas = []  # List of Pizza objects
        self.status = OrderStatus.PLACED

    def add_pizza(self, pizza: Pizza):
        self.pizzas.append(pizza)

    def remove_pizza(self, pizza: Pizza):
        if pizza in self.pizzas:
            self.pizzas.remove(pizza)

    def calculate_total(self) -> float:
        # Sum up the prices of all pizzas in the order.
        return sum(pizza.calculate_price() for pizza in self.pizzas)

    def update_status(self, new_status: OrderStatus):
        # Update the status of the order.
        self.status = new_status

    def _generate_order_id(self) -> str:
        # Generate a unique order id.
        return f"ORD-{uuid.uuid4().hex[:8].upper()}"

    def __str__(self):
        pizzas_details = "\n".join(str(pizza) for pizza in self.pizzas)
        return f"Order ID: {self.id}\nStatus: {self.status.value}\nPizzas:\n{pizzas_details}\nTotal: ${self.calculate_total():.2f}"