# Designing an Elevator System

## Requirements
1. The elevator system should consist of multiple elevators serving multiple floors.
2. Each elevator should have a capacity limit and should not exceed it.
3. Users should be able to request an elevator from any floor and select a destination floor.
4. The elevator system should efficiently handle user requests and optimize the movement of elevators to minimize waiting time.
5. The system should prioritize requests based on the direction of travel and the proximity of the elevators to the requested floor.
6. The elevators should be able to handle multiple requests concurrently and process them in an optimal order.
7. The system should ensure thread safety and prevent race conditions when multiple threads interact with the elevators.

## Classes, Interfaces and Enumerations
1. The **Direction** enum represents the possible directions of elevator movement (UP or DOWN).
2. The **Request** class represents a user request for an elevator, containing the source floor and destination floor.
3. The **Elevator** class represents an individual elevator in the system. It has a capacity limit and maintains a list of 4. requests. The elevator processes requests concurrently and moves between floors based on the requests.
4. The **ElevatorController** class manages multiple elevators and handles user requests. It finds the optimal elevator to serve a request based on the proximity of the elevators to the requested floor.
5. The **ElevatorSystem** class is the entry point of the application and demonstrates the usage of the elevator system.

### Directory Structure

```
elevatorsystem/
├── direction.py
├── elevator.py
├── elevator_controller.py
├── elevator_system_demo.py
└── request.py
```

## **Key Design Considerations and SOLID Principles:**  
> - **Single Responsibility:**  
>   Each class is responsible for a specific aspect of the elevator system. For example, the `Elevator` class manages its own requests and movement, while the `ElevatorController` handles routing user requests to the most appropriate elevator.  
> - **Open/Closed:**  
>   The system is designed to be open for extension (e.g., adding new scheduling policies) without modifying existing code.  
> - **Liskov Substitution:**  
>   The elevator components can be substituted with other implementations (for example, a different scheduling mechanism) as long as they follow the same interface/contract.  
> - **Interface Segregation:**  
>   Each class and method exposes only the functionality that is required for its responsibility (e.g., an elevator’s `process_requests()` method hides the internal details of waiting for requests).  
> - **Dependency Inversion:**  
>   The higher-level modules (such as `ElevatorController`) depend on abstractions (e.g., the request model and public elevator methods) rather than concrete implementations.

### Summary of the Design Steps and SOLID Application

1. **Clarify Requirements and Identify Core Use Cases:**  
   - The system must support multiple elevators serving multiple floors with capacity limits.
   - Users can request an elevator from any floor and the system must optimize movement.

2. **Identify Key Entities:**  
   - **Direction:** An enumeration for elevator movement (UP/DOWN).  
   - **Request:** Represents a user request with source and destination floors.  
   - **Elevator:** Represents an individual elevator that processes its own requests.  
   - **ElevatorController:** Manages multiple elevators and routes requests efficiently.

3. **Define Classes, Interfaces, and Their Attributes:**  
   - Each class is defined in its own file with clear responsibilities and attributes.
   - For example, the `Elevator` class encapsulates current floor, direction, and pending requests.

4. **Determine Core Methods Based on Use Cases:**  
   - Public methods include `add_request()`, `process_requests()`, and `run()` in `Elevator`.
   - `ElevatorController` implements methods such as `request_elevator()` and `find_optimal_elevator()`.

5. **Define Relationships Between Classes:**  
   - **Aggregation/Composition:**  
     - The `ElevatorController` aggregates multiple `Elevator` instances.  
     - Each `Elevator` maintains a list of `Request` objects.
   - **Interaction:**  
     - The controller delegates incoming requests to the best-suited elevator based on proximity.

6. **Implement Necessary Methods:**  
   - Each class implements the required functionality (e.g., safe request handling with locks in `Elevator`).

7. **Exception Handling and Concurrency:**  
   - The use of thread locks and condition variables in `Elevator` ensures thread safety.
   - Elevator threads continuously process requests while new ones are added concurrently.

8. **Follow Good Coding Practices:**  
   - Clear and meaningful class names, method names, and modular design ensure maintainability.
   - The system is extensible and changes (such as alternative scheduling algorithms) can be made with minimal impact on other components.

9. **Apply Design Patterns and SOLID Principles:**  
   - **Single Responsibility:** Each class has a focused responsibility.  
   - **Open/Closed:** The system is designed for extension (for example, a new strategy in the controller) without modifying existing code.  
   - **Liskov Substitution & Interface Segregation:** Classes can be replaced or extended as long as they fulfill the expected behavior.  
   - **Dependency Inversion:** High-level modules (like `ElevatorController`) depend on abstractions (e.g., the public methods of `Elevator`) rather than low-level details.