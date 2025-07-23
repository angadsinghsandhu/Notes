# ================================================================
# File: loadbalancer/least_connection_load_balancer.py
# Description:
#   Implements load balancing using the least connection algorithm.
#
# SOLID:
# - OCP: Can extend LoadBalancer without modifying it.
# ================================================================

from load_balancer import LoadBalancer
from destination import Destination
from request import Request

class LeastConnectionLoadBalancer(LoadBalancer):
    def balance_load(self, request: Request) -> Destination:
        destinations = self.get_destinations(request)
        # Select the destination with the minimum number of requests being served.
        if not destinations:
            raise Exception("No destinations available for request type: " + str(request.request_type))
        # Using min with a lambda that returns the current number of requests being served.
        return min(destinations, key=lambda d: d.requests_being_served)