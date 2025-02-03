# ================================================================
# File: loadbalancer/service.py
# Description:
#   Represents a Service that has a set of Destinations.
#
# SOLID:
# - SRP: Only responsible for maintaining destinations.
# ================================================================

from destination import Destination

class Service:
    def __init__(self, name: str):
        self.name = name
        self.destinations = set()

    def add_destination(self, destination: Destination):
        self.destinations.add(destination)

    def remove_destination(self, destination: Destination):
        self.destinations.discard(destination)