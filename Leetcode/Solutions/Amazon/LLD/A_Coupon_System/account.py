# ================================================================
# File: account.py
# Description:
#   Represents a user’s account with email, password and status.
#
# Steps Covered:
# 2. Identify Key Entities.
# ================================================================

from enum import Enum

class AccountStatus(Enum):
    ACTIVE = 1
    INACTIVE = 2

class Account:
    def __init__(self, email: str, password: str, status: AccountStatus = AccountStatus.ACTIVE):
        self.__email = email
        self.__password = password
        self.__status = status

    def reset_password(self, new_password: str):
        self.__password = new_password