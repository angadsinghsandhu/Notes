# ================================================================
# File: pizza_ordering/order_status.py
# Description:
#   Defines possible order statuses.
#   - Helps track the progress of an order.
#
# Steps Covered:
# 2. Identify Key Entities.
# ================================================================

from enum import Enum

class OrderStatus(Enum):
    PLACED = "Placed"
    PREPARING = "Preparing"
    BAKING = "Baking"
    READY = "Ready"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"