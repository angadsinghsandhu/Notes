# ================================================================
# File: loadbalancer/round_robin_load_balancer.py
# Description:
#   Implements load balancing using the round-robin algorithm.
#   Maintains a queue for each request type.
#
# SOLID:
# - DIP: Depends on the abstract LoadBalancer, not on concrete details.
# ================================================================

from collections import deque
from load_balancer import LoadBalancer
from destination import Destination
from request import Request

class RoundRobinLoadBalancer(LoadBalancer):
    def __init__(self):
        super().__init__()
        # Mapping from request type to a deque (queue) of Destination objects.
        self.destinations_for_request = {}

    def balance_load(self, request: Request) -> Destination:
        if request.request_type not in self.destinations_for_request:
            # Initialize queue from set of destinations.
            destinations = self.get_destinations(request)
            if not destinations:
                raise Exception("No destinations available for request type: " + str(request.request_type))
            self.destinations_for_request[request.request_type] = deque(destinations)
        # Rotate the queue to implement round-robin.
        destination = self.destinations_for_request[request.request_type].popleft()
        self.destinations_for_request[request.request_type].append(destination)
        return destination