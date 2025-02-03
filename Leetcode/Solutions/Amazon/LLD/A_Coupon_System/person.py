# ================================================================
# File: person.py
# Description:
#   Base class for both Admin and User.
#
# Steps Covered:
# 2. Identify Key Entities.
# ================================================================

class Person:
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age

    def get_age(self) -> int:
        return self._age

    def get_name(self) -> str:
        return self._name