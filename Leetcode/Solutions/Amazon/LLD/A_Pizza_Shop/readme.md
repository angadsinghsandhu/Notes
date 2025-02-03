# Pizza Ordering System Low Level Design

Below is an example Low Level Design (LLD) for a **Pizza Ordering System**. This design supports customizing pizzas, tracking orders, and managing inventory. The design follows the SOLID principles and includes inline comments that reference our design steps.

> **Key Points and SOLID Application:**
> - **Single Responsibility:**  
>   Each class is focused on a specific part of the system (e.g., `Pizza` handles customization details, `Order` encapsulates order tracking, and `Inventory` manages ingredient stocks).  
> - **Open/Closed:**  
>   The system is open for extension (for example, adding new toppings or crust types) but closed for modification.  
> - **Liskov Substitution:**  
>   New classes (e.g., new pizza types or order modifications) can replace existing ones without affecting the overall system.  
> - **Interface Segregation:**  
>   Classes expose only the methods required by their clients.  
> - **Dependency Inversion:**  
>   High-level modules depend on abstractions (e.g., an interface for inventory management) rather than on concrete implementations.

## Directory Structure

```
pizza_ordering/
├── crust.py
├── inventory.py
├── order.py
├── order_status.py
├── pizza.py
├── pizza_ordering_system.py
├── topping.py
└── pizza_ordering_system_demo.py
```

## Summary of Design Steps and SOLID Application

1. **Clarify Requirements and Identify Core Use Cases:**
   - The system supports pizza customization (size, crust, toppings), order tracking (from placement to delivery), and inventory management for ingredients.

2. **Identify Key Entities:**
   - **Pizza, Order, Inventory, Crust, Topping, OrderStatus.**

3. **Define Classes and Their Attributes:**
   - Classes like `Pizza` manage customization details.
   - `Order` encapsulates a collection of pizzas and tracks order status.
   - `Inventory` keeps track of available toppings.

4. **Determine Core Methods Based on Use Cases:**
   - Methods such as `add_topping()`, `calculate_price()`, `place_order()`, and `update_order_status()` are implemented to support customization and order flow.

5. **Define Relationships Between Classes:**
   - **Composition:** An `Order` is composed of one or more `Pizza` objects.
   - **Aggregation:** The `PizzaOrderingSystem` manages a collection of orders and an `Inventory` instance.

6. **Implement Necessary Methods:**
   - All core functionalities (e.g., creating orders, updating inventory) are implemented with clear method responsibilities.

7. **Exception Handling and Edge Cases:**
   - Inventory deductions throw errors if there is insufficient stock.
   - Order retrieval and status updates validate order existence.

8. **Follow Good Coding Practices:**
   - Meaningful naming, modular design, and clear separation of concerns.
   - The Singleton pattern is used in `PizzaOrderingSystem` to manage global state.

9. **Apply Design Patterns and Principles:**
   - **Singleton Pattern:** Used for the ordering system.
   - **Strategy Pattern (potential):** Can be applied for payment or discount strategies in future enhancements.
   - Adherence to SOLID principles ensures that the system is extensible and maintainable.