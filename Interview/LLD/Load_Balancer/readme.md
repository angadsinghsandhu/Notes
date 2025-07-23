# Load Balancer

Below is an example Low Level Design (LLD) for a **Load Balancer System** written in Python. This design follows the SOLID principles and is organized into several files. In our design, we provide a common abstract base class `LoadBalancer` and several concrete implementations that use different load balancing algorithms (e.g., least connections, round-robin, routed). We also include supporting classes such as `Service`, `Request`, `Destination`, and an enumeration for `RequestType`. A factory class is also provided to instantiate the appropriate load balancer.

### Directory Structure

```
loadbalancer/
├── __init__.py
├── load_balancer.py
├── least_connection_load_balancer.py
├── routed_load_balancer.py
├── round_robin_load_balancer.py
├── service.py
├── request.py
├── destination.py
├── request_type.py
├── load_balancer_factory.py
└── demo.py
```

## **SOLID & Design Considerations:**
> 
> - **Single Responsibility Principle (SRP):**  
>   Each class is responsible for a single concept. For example, the `LoadBalancer` (and its subclasses) handle request routing, while the `Service` class manages its list of destinations.
> 
> - **Open/Closed Principle (OCP):**  
>   New load balancing algorithms can be added by extending the `LoadBalancer` abstract class without modifying existing code.
> 
> - **Liskov Substitution Principle (LSP):**  
>   All subclasses of `LoadBalancer` implement the `balance_load` method, so they can be used interchangeably.
> 
> - **Interface Segregation Principle (ISP):**  
>   The abstract base class exposes only the methods required by clients (e.g., `register`, `balance_load`).
> 
> - **Dependency Inversion Principle (DIP):**  
>   High-level modules (such as the `LoadBalancerFactory`) depend on abstractions (the `LoadBalancer` base class) rather than on concrete implementations.
> 
> ---

### Summary

1. **Clarify Requirements and Identify Use Cases:**  
   - The system must route incoming requests to the appropriate destination based on various algorithms (least connection, round-robin, routed, etc.).

2. **Identify Key Entities:**  
   - **LoadBalancer (abstract):** Base class for load balancers.
   - **Concrete LoadBalancers:** LeastConnectionLoadBalancer, RoundRobinLoadBalancer, RoutedLoadBalancer.
   - **Service:** Manages a set of Destinations.
   - **Request:** Contains the request’s ID, type, and parameters.
   - **Destination:** Represents a server instance with current load and a request threshold.
   - **RequestType:** Enumeration for different kinds of requests.
   - **LoadBalancerFactory:** Creates load balancer instances based on a string identifier.

3. **Define Classes and Their Responsibilities:**  
   - Each file is dedicated to one class or concept (e.g., service, destination, request).
   - The abstract class defines the common interface while concrete implementations override the load balancing algorithm.

4. **Determine Core Methods:**  
   - `register()`, `get_destinations()`, and the abstract `balance_load()` in `LoadBalancer`.
   - Concrete load balancers implement `balance_load()` using their respective algorithms.

5. **SOLID Principles:**  
   - **SRP:** Each class has a focused responsibility.
   - **OCP:** New load balancing strategies can be added via subclassing.
   - **LSP:** All load balancers can be used interchangeably.
   - **ISP:** The interfaces expose only necessary methods.
   - **DIP:** High-level modules depend on abstractions (e.g., `LoadBalancer`) and are decoupled from concrete implementations.