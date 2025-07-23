# ================================================================
# File: loadbalancer/load_balancer_factory.py
# Description:
#   Factory class to create instances of LoadBalancer based on the given type.
#
# SOLID:
# - DIP: Clients depend on the abstraction (LoadBalancer) rather than concrete classes.
# ================================================================

from least_connection_load_balancer import LeastConnectionLoadBalancer
from round_robin_load_balancer import RoundRobinLoadBalancer
from routed_load_balancer import RoutedLoadBalancer

class LoadBalancerFactory:
    @staticmethod
    def create_load_balancer(lb_type: str):
        lb_type = lb_type.lower()
        if lb_type == "round-robin":
            return RoundRobinLoadBalancer()
        elif lb_type == "least-connection":
            return LeastConnectionLoadBalancer()
        elif lb_type == "routed":
            return RoutedLoadBalancer()
        else:
            # Default to least connection if not specified.
            return LeastConnectionLoadBalancer()