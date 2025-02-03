# ================================================================
# File: loadbalancer/request_type.py
# Description:
#   Enumerates different types of requests.
#
# SOLID:
# - SRP: Only responsible for representing request types.
# ================================================================

from enum import Enum

class RequestType(Enum):
    # Example request types; these can be extended as needed.
    READ = 1
    WRITE = 2
    UPDATE = 3