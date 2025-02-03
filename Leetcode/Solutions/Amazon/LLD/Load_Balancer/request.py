# ================================================================
# File: loadbalancer/request.py
# Description:
#   Represents a Request coming into the load balancer.
#
# SOLID:
# - SRP: Encapsulates only request-related data.
# ================================================================

from request_type import RequestType

class Request:
    def __init__(self, id: str, request_type: RequestType, parameters: dict = None):
        self.id = id
        self.request_type = request_type
        self.parameters = parameters or {}