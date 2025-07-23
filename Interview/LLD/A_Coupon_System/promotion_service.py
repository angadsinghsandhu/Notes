# ================================================================
# File: promotion_service.py
# Description:
#   Defines an interface (or abstract base class) for promotion CRUD operations.
#   Concrete services for Coupons and Vouchers will implement these methods.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Interfaces.
# ================================================================

from abc import ABC, abstractmethod

class PromotionService(ABC):
    @abstractmethod
    def add_promotion(self, promotion):
        pass

    @abstractmethod
    def update_promotion(self, promotion):
        pass

    @abstractmethod
    def delete_promotion(self, promotion_id: int):
        pass

    @abstractmethod
    def get_promotions(self, user_id: str = None):
        pass

    @abstractmethod
    def apply_promotion(self, user, transaction, promotion_code: str) -> bool:
        pass