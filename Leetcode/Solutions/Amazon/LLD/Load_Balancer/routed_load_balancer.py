# ================================================================
# File: loadbalancer/routed_load_balancer.py
# Description:
#   Implements load balancing by routing based on a hash of the request id.
#
# SOLID:
# - LSP: Inherits LoadBalancer and implements balance_load appropriately.
# ================================================================

from load_balancer import LoadBalancer
from destination import Destination
from request import Request

class RoutedLoadBalancer(LoadBalancer):
    def balance_load(self, request: Request) -> Destination:
        destinations = list(self.get_destinations(request))
        if not destinations:
            raise Exception("No destinations available for request type: " + str(request.request_type))
        # Hash-based routing: using modulo of the hash of the request id.
        index = hash(request.id) % len(destinations)
        return destinations[index]