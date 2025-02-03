# ================================================================
# File: product.py
# Description:
#   Represents a product listing in the system.
#   A product has a unique ID, name, description, and a recommended
#   minimum storage type. (For example, a product that is small might be stored
#   in a small locker; but if small lockers are full, medium or large may be used.)
#
# SOLID:
# - SRP: Handles only product metadata.
# ================================================================

from locker_type import LockerType

class Product:
    def __init__(self, product_id: str, name: str, description: str, recommended_locker: LockerType):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.recommended_locker = recommended_locker