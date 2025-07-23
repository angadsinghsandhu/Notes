# ================================================================
# File: pizza_ordering/pizza_ordering_system.py
# Description:
#   Core class that manages the pizza ordering process.
#   - Allows customers to create orders, customize pizzas, track orders, and update inventory.
#   - Follows the Singleton pattern to ensure one central system.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 2. Identify Key Entities.
# 4. Determine Core Methods Based on Use Cases.
# 6. Implement Necessary Methods.
# ================================================================

from order import Order
from inventory import Inventory
from order_status import OrderStatus

class PizzaOrderingSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize orders and inventory.
            cls._instance.orders = {}
            cls._instance.inventory = Inventory()
        return cls._instance

    def create_order(self) -> Order:
        # Create a new order and store it in the system.
        order = Order()
        self.orders[order.id] = order
        return order

    def get_order(self, order_id: str):
        # Retrieve an order by its id.
        return self.orders.get(order_id)

    def place_order(self, order: Order):
        # Before finalizing the order, update the inventory.
        self.inventory.update_for_order(order.pizzas)
        order.update_status(OrderStatus.PREPARING)
        # In a full implementation, additional steps such as payment processing
        # and order tracking notifications would be added here.
        self.orders[order.id] = order
        return order

    def update_order_status(self, order_id: str, new_status: OrderStatus):
        # Update the status of an existing order.
        order = self.get_order(order_id)
        if order:
            order.update_status(new_status)
            return order
        else:
            raise ValueError("Order not found.")