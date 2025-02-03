# Designing a Vending Machine

## Requirements
1. The vending machine should support multiple products with different prices and quantities.
1. The machine should accept coins and notes of different denominations.
1. The machine should dispense the selected product and return change if necessary.
1. The machine should keep track of the available products and their quantities.
1. The machine should handle multiple transactions concurrently and ensure data consistency.
1. The machine should provide an interface for restocking products and collecting money.
1. The machine should handle exceptional scenarios, such as insufficient funds or out-of-stock products.

## Directory Structure

```
vendingmachine/
├── coin.py
├── dispense_state.py
├── idle_state.py
├── inventory.py
├── note.py
├── product.py
├── ready_state.py
├── return_change_state.py
├── vending_machine.py
├── vending_machine_demo.py
└── vending_machine_state.py
```

## Classes, Interfaces and Enumerations
1. The **Product** class represents a product in the vending machine, with properties such as name and price.
2. The **Coin** and **Note** enums represent the different denominations of coins and notes accepted by the vending machine.
3. The **Inventory** class manages the available products and their quantities in the vending machine. It uses a concurrent hash map to ensure thread safety.
4. The **VendingMachineState** interface defines the behavior of the vending machine in different states, such as idle, ready, and dispense.
5. The **IdleState**, **ReadyState**, and **DispenseState** classes implement the VendingMachineState interface and define the specific behaviors for each state.
6. The **VendingMachine** class is the main class that represents the vending machine. It follows the Singleton pattern to ensure only one instance of the vending machine exists.
7. The VendingMachine class maintains the current state, selected product, total payment, and provides methods for state transitions and payment handling.
8. The **VendingMachineDemo** class demonstrates the usage of the vending machine by adding products to the inventory, selecting products, inserting coins and notes, dispensing products, and returning change.

## **Key Design Considerations and SOLID Principles:**  
> - **Single Responsibility:**  
>   Each class handles a specific responsibility. For example, the `Product` class represents an individual product, while each state class (e.g., `IdleState`, `ReadyState`) encapsulates behavior for that state.  
> - **Open/Closed:**  
>   The vending machine behavior can be extended (by adding new states or payment methods) without modifying existing code.  
> - **Liskov Substitution:**  
>   All state classes implement the same `VendingMachineState` interface so they can be interchanged seamlessly.  
> - **Interface Segregation:**  
>   The `VendingMachineState` interface defines only the necessary operations that each state must support.  
> - **Dependency Inversion:**  
>   The high-level `VendingMachine` class depends on the abstraction (`VendingMachineState`) rather than concrete implementations.

### Summary of the Design Steps and SOLID Application

1. **Clarify Requirements and Identify Core Use Cases:**  
   - The vending machine must support multiple products, accept coins/notes, dispense products with change, and handle concurrent transactions.

2. **Identify Key Entities:**  
   - **Product:** Represents individual products.
   - **Coin/Note:** Represent payment denominations.
   - **Inventory:** Manages product stock.
   - **VendingMachineState and Concrete States:** Define behaviors (Idle, Ready, Dispense, Return Change).
   - **VendingMachine:** Main controller (Singleton) managing state transitions and payment processing.

3. **Define Classes, Interfaces, and Their Attributes:**  
   - Each file defines a distinct class or interface with focused responsibilities.

4. **Determine Core Methods Based on Use Cases:**  
   - Methods such as `select_product`, `insert_coin`, `insert_note`, `dispense_product`, and `return_change` are defined and implemented in each state.

5. **Define Relationships Between Classes:**  
   - **Composition:** `VendingMachine` aggregates an `Inventory` and various state instances.
   - **State Pattern:** Different behaviors are encapsulated in separate state classes implementing `VendingMachineState`.

6. **Implement Necessary Methods:**  
   - Each state class implements the required interface methods to ensure proper state transitions and actions.

7. **Exception Handling and Edge Cases:**  
   - Methods provide user feedback for invalid actions (e.g., selecting a product when none is available or inserting coins before product selection).

8. **Follow Good Coding Practices:**  
   - Meaningful naming, modular design, and separation of concerns are maintained throughout the implementation.

9. **Apply Design Patterns and SOLID Principles:**  
   - The **Singleton Pattern** ensures only one instance of `VendingMachine`.
   - The **State Pattern** cleanly separates state-specific behaviors.
   - **SOLID principles** are followed in class design and method responsibilities.