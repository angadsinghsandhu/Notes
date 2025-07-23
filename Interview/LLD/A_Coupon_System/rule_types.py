# ================================================================
# File: rule_types.py
# Description:
#   Enumerates the different types of rules that can be applied.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Enumerations.
# ================================================================

from enum import Enum

class RuleTypes(Enum):
    AGE_LIMIT = 1
    TRANSACTION_VALUE_LIMIT = 2
    USAGE_LIMIT = 3