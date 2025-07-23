# ================================================================
# File: pizza_ordering/pizza_ordering_system_demo.py
# Description:
#   Acts as the entry point for the Pizza Ordering System demo.
#   - Demonstrates creating a custom pizza, placing an order, and updating order status.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 6. Implement Necessary Methods.
# 8. Follow Good Coding Practices.
# ================================================================

from pizza_ordering_system import PizzaOrderingSystem
from pizza import Pizza
from crust import Crust
from topping import Topping
from order_status import OrderStatus

class PizzaOrderingSystemDemo:
    @staticmethod
    def run():
        system = PizzaOrderingSystem()

        # Create a new order.
        order = system.create_order()
        print(f"New Order Created: {order.id}")

        # Create a custom pizza.
        pizza1 = Pizza("Large", Crust.STUFFED)
        pizza1.add_topping(Topping.PEPPERONI)
        pizza1.add_topping(Topping.EXTRA_CHEESE)
        pizza1.add_topping(Topping.ONIONS)
        # Add the pizza to the order.
        order.add_pizza(pizza1)

        # Place the order (this will update inventory and change order status).
        system.place_order(order)
        print("Order placed. Current order details:")
        print(order)

        # Update the order status as the order progresses.
        system.update_order_status(order.id, OrderStatus.BAKING)
        print(f"Order status updated to: {order.status.value}")

        system.update_order_status(order.id, OrderStatus.READY)
        print(f"Order status updated to: {order.status.value}")

        system.update_order_status(order.id, OrderStatus.DELIVERED)
        print(f"Order status updated to: {order.status.value}")

if __name__ == "__main__":
    PizzaOrderingSystemDemo.run()