# ================================================================
# File: hotelmanagement/guest.py
# Description:
#   Represents a hotel guest with an id, name, email, and phone number.
#   - Follows the Single Responsibility Principle.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# ================================================================

class Guest:
    def __init__(self, guest_id: str, name: str, email: str, phone_number: str):
        self._id = guest_id
        self._name = name
        self._email = email
        self._phone_number = phone_number

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def phone_number(self) -> str:
        return self._phone_number