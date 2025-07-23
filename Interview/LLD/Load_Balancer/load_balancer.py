# ================================================================
# File: loadbalancer/load_balancer.py
# Description:
#   Defines the abstract base class for a Load Balancer.
#   Provides common methods such as register and get_destinations.
#
# SOLID:
# - SRP: Only deals with load balancer registration and common retrieval.
# - ISP: Exposes only the necessary interface (balance_load) for clients.
# ================================================================

from abc import ABC, abstractmethod
from service import Service
from request import Request

class LoadBalancer(ABC):
    def __init__(self):
        # Map of request type to Service
        self.service_map = {}
    
    def register(self, request_type, service: Service):
        self.service_map[request_type] = service

    def get_destinations(self, request: Request):
        service = self.service_map.get(request.request_type)
        if service:
            return service.destinations
        return set()

    @abstractmethod
    def balance_load(self, request: Request):
        """Abstract method to be implemented by subclasses for load balancing."""
        pass