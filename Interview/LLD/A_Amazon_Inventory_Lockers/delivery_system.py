# ================================================================
# File: delivery_system.py
# Description:
#   Represents the central Delivery System.
#   Maintains a registry of lockers and products, and provides APIs for:
#     - Scanning a QR code to retrieve product/item information.
#     - Adding (onboarding) a new product (and its item) into the system.
#     - Finding an appropriate locker using a storage strategy.
#     - Removing (emptying) a locker.
#     - Retrieving the locker where a certain product (or item) is stored.
#
# SOLID:
# - SRP: This class coordinates system operations.
# - DIP: It depends on abstractions like StorageStrategy.
# ================================================================

from locker import Locker
from product import Product
from item import Item
from storage_strategy import StorageStrategy

class DeliverySystem:
    def __init__(self):
        # Registry of lockers (map locker_id -> Locker)
        self.lockers = {}
        # Registry of products (map product_id -> Product)
        self.products = {}
        # Registry of items (map item_id -> Item)
        self.item_registry = {}
        # We can use a storage strategy to choose a locker for an item.
        self.storage_strategy = StorageStrategy()

    def add_locker(self, locker: Locker):
        self.lockers[locker.locker_id] = locker

    def add_product(self, product: Product):
        self.products[product.product_id] = product
        print(f"Product {product.name} listed.")

    def onboard_item(self, item: Item):
        # When a new item arrives, choose an appropriate locker.
        # Get a list of all lockers.
        available_lockers = list(self.lockers.values())
        chosen_locker = self.storage_strategy.choose_locker(item, available_lockers)
        chosen_locker.add_item(item)
        # Register the item.
        self.item_registry[item.item_id] = item

    def remove_item(self, locker_id: str):
        if locker_id not in self.lockers:
            raise Exception("Locker not found.")
        locker = self.lockers[locker_id]
        removed_item = locker.remove_item()
        # Remove from registry.
        if removed_item.item_id in self.item_registry:
            del self.item_registry[removed_item.item_id]
        return removed_item

    def find_locker_for_item(self, item_id: str):
        # Returns the locker where the item is placed.
        if item_id in self.item_registry:
            return self.item_registry[item_id].locker
        else:
            raise Exception("Item not found in the system.")

    def scan_qr(self, qr_code: str):
        """
        Simulate scanning a QR code.
        For simplicity, assume the QR code contains the item ID.
        Returns the associated item.
        """
        if qr_code in self.item_registry:
            item = self.item_registry[qr_code]
            print(f"QR scan: Retrieved {item}")
            return item
        else:
            raise Exception("QR code not recognized.")