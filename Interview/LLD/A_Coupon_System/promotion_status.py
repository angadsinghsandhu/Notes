# ================================================================
# File: promotion_status.py
# Description:
#   Enumerates possible statuses for a coupon/voucher.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Enumerations.
# ================================================================

from enum import Enum

class PromotionStatus(Enum):
    ACTIVE = 1
    INACTIVE = 2