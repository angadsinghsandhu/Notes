# ================================================================
# File: storage_strategy.py
# Description:
#   Implements a strategy for choosing the best locker for an item.
#   The strategy considers the product’s recommended locker type as well as
#   the distance of available lockers from the system.
#
# SOLID:
# - OCP: New strategies can be added by implementing the StorageStrategy interface.
# - DIP: High-level modules depend on this abstraction.
# ================================================================

from locker_type import LockerType

class StorageStrategy:
    def choose_locker(self, item, lockers: list):
        """
        Chooses the optimal locker for the given item from the list of available lockers.
        Rules (example):
          - If the product is small, it can go in SMALL, MEDIUM, or LARGE.
          - If the product is medium, it can go in MEDIUM or LARGE.
          - If the product is large, it goes only in LARGE.
          - Among eligible lockers, choose the one with the smallest distance.
        """
        eligible_lockers = []
        recommended = item.product.recommended_locker
        for locker in lockers:
            # Check if locker type is eligible:
            if locker.is_empty():
                # A simple eligibility check:
                if recommended == LockerType.SMALL:
                    eligible_lockers.append(locker)
                elif recommended == LockerType.MEDIUM:
                    if locker.locker_type in [LockerType.MEDIUM, LockerType.LARGE]:
                        eligible_lockers.append(locker)
                elif recommended == LockerType.LARGE:
                    if locker.locker_type == LockerType.LARGE:
                        eligible_lockers.append(locker)
        if not eligible_lockers:
            raise Exception("No eligible locker available for item " + item.item_id)
        # Choose the eligible locker with minimum distance.
        chosen = min(eligible_lockers, key=lambda l: l.distance)
        return chosen