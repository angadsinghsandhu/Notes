# ================================================================
# File: locker.py
# Description:
#   Represents a Locker (storage unit) in the system.
#   Each locker has a unique ID, a type (Small, Medium, Large), a distance
#   from the system (to help choose optimal lockers), and may hold one Item.
#
# SOLID:
# - SRP: Responsible only for locker state and basic operations (add/remove).
# ================================================================

from locker_type import LockerType

class Locker:
    def __init__(self, locker_id: str, locker_type: LockerType, distance: float):
        self.locker_id = locker_id
        self.locker_type = locker_type
        self.distance = distance  # distance from the system (could be in meters)
        self.item = None  # Initially empty

    def is_empty(self) -> bool:
        return self.item is None

    def add_item(self, item):
        if not self.is_empty():
            raise Exception(f"Locker {self.locker_id} is already occupied.")
        self.item = item
        # Set the locker reference in the item
        item.set_locker(self)
        print(f"Item {item.item_id} placed in locker {self.locker_id}.")

    def remove_item(self):
        if self.is_empty():
            raise Exception(f"Locker {self.locker_id} is already empty.")
        removed_item = self.item
        self.item = None
        # Clear the locker reference in the item
        removed_item.set_locker(None)
        print(f"Locker {self.locker_id} is now empty.")
        return removed_item