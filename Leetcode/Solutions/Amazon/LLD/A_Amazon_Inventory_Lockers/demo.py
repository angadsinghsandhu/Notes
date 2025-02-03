# ================================================================
# File: delivery_system_demo.py
# Description:
#   Demonstrates the end-to-end functionality of the Delivery & Locker Management System.
#
# Steps Covered:
# 1. Instantiate and configure the system.
# 2. List new products.
# 3. Onboard a new item (simulate package arrival) using a delivery agent.
# 4. Scan a QR code to retrieve package (item) information.
# 5. Retrieve locker information for a given item.
# ================================================================

from locker_type import LockerType
from locker import Locker
from product import Product
from item import Item
from delivery_system import DeliverySystem
from delivery_agent import DeliveryAgent

def main():
    # Initialize the central delivery system.
    system = DeliverySystem()
    
    # Add some lockers to the system.
    locker1 = Locker("L1", LockerType.SMALL, distance=5.0)
    locker2 = Locker("L2", LockerType.MEDIUM, distance=3.0)
    locker3 = Locker("L3", LockerType.LARGE, distance=10.0)
    system.add_locker(locker1)
    system.add_locker(locker2)
    system.add_locker(locker3)
    
    # List a new product.
    product = Product("P1", "Wireless Mouse", "A compact wireless mouse", LockerType.SMALL)
    system.add_product(product)
    
    # Create a new item (instance of the product).
    item = Item("I1", product)
    
    # Create a Delivery Agent.
    agent = DeliveryAgent("AgentA", system)
    
    # The delivery agent onboards the new package (item) into the system.
    agent.onboard_new_package(item)
    
    # Simulate scanning the QR code on the package.
    # (In our simulation, the QR code is the item ID.)
    agent.deliver_package("I1")
    
    # Check in the system to see which locker holds the item.
    locker_found = system.find_locker_for_item("I1")
    print(f"Item I1 is placed in locker {locker_found.locker_id} (Type: {locker_found.locker_type.name}, Distance: {locker_found.distance}).")
    
    # Optionally, simulate emptying a locker.
    removed_item = system.remove_item(locker_found.locker_id)
    print(f"Removed {removed_item} from locker {locker_found.locker_id}.")

if __name__ == "__main__":
    main()