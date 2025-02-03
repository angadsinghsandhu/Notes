# ================================================================
# File: rule.py
# Description:
#   Abstract class representing a validation rule for a promotion.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Interfaces/Abstract Classes.
# ================================================================

from abc import ABC, abstractmethod
from rule_types import RuleTypes

class Rule(ABC):
    def __init__(self, name: str, rule_type: RuleTypes):
        self._name = name
        self._rule_type = rule_type

    @abstractmethod
    def can_apply(self, user, transaction, coupon) -> bool:
        pass