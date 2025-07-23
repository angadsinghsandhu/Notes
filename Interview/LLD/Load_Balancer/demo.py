# ================================================================
# File: loadbalancer/load_balancer_demo.py
# Description:
#   Demonstrates the usage of the Load Balancer system.
#   - Creates a service with multiple destinations.
#   - Registers the service for a specific request type.
#   - Creates a request and uses a load balancer (via the factory)
#     to route the request to an optimal destination.
#
# Steps Covered:
# 1. Instantiate and configure the system.
# 2. Demonstrate the load balancing behavior.
# 8. Follow Good Coding Practices.
#
# SOLID:
# - DIP: Clients depend on the abstract LoadBalancer interface.
# ================================================================

from load_balancer_factory import LoadBalancerFactory
from request import Request
from request_type import RequestType
from service import Service
from destination import Destination

def main():
    # Create a service with some destinations.
    service = Service("ExampleService")
    # Create some Destination instances with simulated IPs and thresholds.
    dest1 = Destination("192.168.1.1", threshold=10)
    dest2 = Destination("192.168.1.2", threshold=10)
    dest3 = Destination("192.168.1.3", threshold=10)
    
    # Add destinations to the service.
    service.add_destination(dest1)
    service.add_destination(dest2)
    service.add_destination(dest3)
    
    # Create a load balancer instance using the factory.
    # For example, we choose "round-robin" here.
    lb = LoadBalancerFactory.create_load_balancer("round-robin")
    
    # Register the service for a specific request type.
    lb.register(RequestType.READ, service)
    
    # Create a sample request.
    request = Request(id="req-1001", request_type=RequestType.READ, parameters={"param": "value"})
    
    # Route the request using the load balancer.
    destination = lb.balance_load(request)
    
    print(f"Request {request.id} routed to destination with IP: {destination.ip_address}")

    # Optionally, simulate multiple requests to see round-robin behavior.
    for i in range(5):
        req = Request(id=f"req-{1002+i}", request_type=RequestType.READ)
        dest = lb.balance_load(req)
        print(f"Request {req.id} routed to destination with IP: {dest.ip_address}")

if __name__ == "__main__":
    main()
