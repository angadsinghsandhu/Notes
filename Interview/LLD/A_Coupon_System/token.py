# ================================================================
# File: token.py
# Description:
#   Abstract base class representing a promotional token.
#   It captures common properties like expiry, name, description, creator and status.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# ================================================================

from abc import ABC
from datetime import datetime, timedelta
from promotion_status import PromotionStatus

class Token(ABC):
    def __init__(self, expiry_duration_in_days: int, name: str, description: str, creator: str, 
                 status: PromotionStatus = PromotionStatus.ACTIVE):
        self.__created_at = datetime.now()
        self.__expiry_time = datetime.now() + timedelta(days=expiry_duration_in_days)
        self.__name = name
        self.__description = description
        self.__status = status
        self.__created_by = creator

    # Assume getters/setters are defined (omitted for brevity)
    def is_expired(self) -> bool:
        return datetime.now() > self.__expiry_time