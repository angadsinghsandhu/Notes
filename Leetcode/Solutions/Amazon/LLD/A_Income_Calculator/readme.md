# Income Calculator Low Level Design

Below is an example Low Level Design (LLD) for an **Income Calculator** system. This design calculates the net income based on a user’s base salary, bonuses, and deductions. The design follows SOLID principles and includes inline comments that reference our design steps.

## **SOLID Highlights:**
> - **Single Responsibility:**  
>   Each class is focused on one aspect of the income calculation process (e.g., `Salary`, `Bonus`, and `Deduction` hold individual financial data, `IncomeData` aggregates these, and `IncomeCalculator` performs the calculation).
> - **Open/Closed:**  
>   The system is open for extension (e.g., you can later add additional income components or complex calculation strategies) but closed for modification.
> - **Liskov Substitution:**  
>   Each component can be replaced or extended (for example, if you want to change how bonuses are applied) without altering the calculator’s core logic.
> - **Interface Segregation:**  
>   The design exposes only the necessary operations for each entity (e.g., a calculator only needs a method to compute net income).
> - **Dependency Inversion:**  
>   High-level modules (e.g., the demo or user interface) depend on abstractions such as `IncomeCalculator` and `IncomeData` rather than concrete implementations of input components.

## Directory Structure

```
income_calculator/
├── bonus.py
├── deduction.py
├── income_calculator.py
├── income_calculator_demo.py
├── income_data.py
└── salary.py
```

## Summary of Design Steps and SOLID Application

1. **Clarify Requirements and Identify Core Use Cases:**  
   - The system calculates the net income based on a user’s base salary, bonuses, and deductions.

2. **Identify Key Entities:**  
   - Entities include **Salary**, **Bonus**, **Deduction**, and **IncomeData**.

3. **Define Classes and Their Attributes:**  
   - Each class encapsulates a specific piece of financial data.
   - `IncomeData` aggregates these components into one object.

4. **Determine Core Methods Based on Use Cases:**  
   - `IncomeCalculator.calculate_net_income()` computes the net income.

5. **Define Relationships Between Classes:**  
   - **Composition:** `IncomeData` is composed of a `Salary` object and lists of `Bonus` and `Deduction` objects.
   - The `IncomeCalculator` depends on `IncomeData` to perform its calculation.

6. **Implement Necessary Methods:**  
   - All required functionalities (input aggregation and income computation) are implemented in dedicated classes.

7. **Exception Handling and Edge Cases:**  
   - While this basic implementation assumes valid input, further enhancements can add validation and error handling for production use.

8. **Follow Good Coding Practices:**  
   - Clear separation of concerns, modular design, and meaningful naming are employed throughout the design.

9. **Apply Design Patterns and Principles:**  
   - Adheres to SOLID principles, ensuring that the system is easily extensible (e.g., adding new income components) without requiring modifications to the existing codebase.