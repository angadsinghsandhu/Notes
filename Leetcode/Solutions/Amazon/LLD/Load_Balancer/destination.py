# ================================================================
# File: loadbalancer/destination.py
# Description:
#   Represents a destination (e.g., a server instance) where requests are served.
#
# SOLID:
# - SRP: Handles destination-related data and logic.
# ================================================================

class Destination:
    def __init__(self, ip_address: str, threshold: int):
        self.ip_address = ip_address
        self.requests_being_served = 0
        self.threshold = threshold

    def accept_request(self, request) -> bool:
        if self.requests_being_served < self.threshold:
            self.requests_being_served += 1
            return True
        return False

    def complete_request(self):
        if self.requests_being_served > 0:
            self.requests_being_served -= 1

    def __hash__(self):
        # Ensure Destination is hashable so it can be added to a set.
        return hash(self.ip_address)

    def __eq__(self, other):
        return isinstance(other, Destination) and self.ip_address == other.ip_address