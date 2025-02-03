# ================================================================
# File: basic_calculator/calculator_demo.py
# Description:
#   Demonstrates usage of the Calculator class.
#   - Provides a simple command-line interface for user input.
#   - Handles basic input validation and error handling.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 6. Implement Necessary Methods.
# 8. Follow Good Coding Practices.
# ================================================================

from calculator import Calculator

def main():
    calc = Calculator()
    print("Basic Calculator")
    print("Enter your calculation in the format: operand operator operand")
    print("Supported operators: +, -, *, /")
    
    while True:
        try:
            user_input = input("Calculation (or 'exit' to quit): ")
            if user_input.lower() == "exit":
                break

            # Example input: 10 + 5
            parts = user_input.strip().split()
            if len(parts) != 3:
                print("Invalid input format. Please try again.")
                continue

            operand1, operator, operand2 = parts
            operand1 = float(operand1)
            operand2 = float(operand2)
            
            result = calc.calculate(operand1, operator, operand2)
            print(f"Result: {result}")

        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()