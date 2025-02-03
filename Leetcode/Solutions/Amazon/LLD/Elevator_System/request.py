# ================================================================
# File: elevatorsystem/request.py
# Description:
#   Represents a user request for an elevator.
#   - Contains the source and destination floors.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# ================================================================

class Request:
    def __init__(self, source_floor, destination_floor):
        self.source_floor = source_floor      # Floor where the request originated.
        self.destination_floor = destination_floor  # Floor the user wants to go to.