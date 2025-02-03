# Simple Calculator Lower System Design

Below is an example Low-Level Design (LLD) for a **Basic Calculator** system. This design breaks down the calculator into several components that work together to perform arithmetic operations, handle user inputs, and provide error handling. In this example, we use an object‐oriented approach with SOLID principles in mind. We’ve separated concerns into operation classes, a calculator orchestrator, and a simple user interface (demo). You can extend this design with additional operations (e.g., exponentiation or modulus) or features (e.g., memory functions) as needed.

## **SOLID Highlights:**

 - **Single Responsibility:**  
   Each class has a clear, single responsibility. The operation classes (e.g., Addition, Subtraction) handle one arithmetic operation each. The Calculator class coordinates these operations and user input.

 - **Open/Closed:**  
   The system is open for extension. Adding a new operation simply requires creating a new subclass of the Operation base class and registering it in the Calculator class.

 - **Liskov Substitution:**  
   All operation subclasses can be used interchangeably via the Operation interface.

 - **Interface Segregation:**  
   The Operation base class exposes only one method, keeping the interface minimal.

 - **Dependency Inversion:**  
   The Calculator depends on abstractions (the Operation interface) rather than on concrete implementations.

 ---

## Proposed Directory Structure

```
 basic_calculator/
 ├── operation.py
 ├── addition.py
 ├── subtraction.py
 ├── multiplication.py
 ├── division.py
 ├── calculator.py
 └── calculator_demo.py
```

## Summary of Design Steps and SOLID Application

 1. **Clarify Requirements and Identify Core Use Cases:**  
    - The calculator should perform basic arithmetic operations (addition, subtraction, multiplication, division), validate input, and handle errors (such as division by zero).

 2. **Identify Key Entities:**  
    - **Operation:** An abstract entity for arithmetic operations.
    - **Concrete Operations:** Addition, Subtraction, Multiplication, and Division.
    - **Calculator:** Coordinates operations and user input.

 3. **Define Classes and Their Attributes:**  
    - Each operation class encapsulates one arithmetic operation.
    - The Calculator class maps operation symbols to concrete operation classes.

 4. **Determine Core Methods Based on Use Cases:**  
    - The `operate()` method in each operation class executes the calculation.
    - The Calculator’s `calculate()` method validates the operator and delegates the calculation.

 5. **Define Relationships Between Classes:**  
    - **Composition:** The Calculator class contains a mapping of operations.
    - **Abstraction:** Operation serves as an interface that all concrete operations implement.

 6. **Implement Necessary Methods:**  
    - All required methods are implemented with input parsing, calculation, and error handling.

 7. **Exception Handling and Edge Cases:**  
    - Division by zero is handled with a ValueError in the Division class.
    - Invalid operator input is caught in the Calculator class.

 8. **Follow Good Coding Practices:**  
    - The design uses clear naming, modularity, and separation of concerns.

 9. **Potential Extensions:**  
    - To support new operations (e.g., exponentiation or modulus), create a new subclass of Operation and add it to the Calculator’s dictionary.
    - Additional features such as memory functions can be implemented as separate classes or methods.

This complete LLD demonstrates a modular and extensible approach to designing a basic calculator system, while also addressing error handling, user input validation, and future extensibility—all in line with SOLID design principles.