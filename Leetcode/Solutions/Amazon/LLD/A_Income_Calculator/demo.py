# ================================================================
# File: income_calculator/income_calculator_demo.py
# Description:
#   Acts as the entry point to demonstrate the Income Calculator.
#   - Collects user input for salary, bonuses, and deductions.
#   - Uses IncomeCalculator to compute and display the net income.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 6. Implement Necessary Methods.
# 8. Follow Good Coding Practices.
# ================================================================

from salary import Salary
from bonus import Bonus
from deduction import Deduction
from income_data import IncomeData
from income_calculator import IncomeCalculator

def main():
    # Gather user input for salary.
    salary_amount = float(input("Enter your base salary: "))
    salary = Salary(salary_amount)

    # Gather bonus information.
    bonuses = []
    num_bonuses = int(input("Enter number of bonuses: "))
    for i in range(num_bonuses):
        bonus_amount = float(input(f"Enter bonus {i+1} amount: "))
        bonuses.append(Bonus(bonus_amount, f"Bonus {i+1}"))

    # Gather deduction information.
    deductions = []
    num_deductions = int(input("Enter number of deductions: "))
    for i in range(num_deductions):
        deduction_amount = float(input(f"Enter deduction {i+1} amount: "))
        deductions.append(Deduction(deduction_amount, f"Deduction {i+1}"))

    # Aggregate all income components into IncomeData.
    income_data = IncomeData(salary, bonuses, deductions)
    # Create the calculator instance.
    calculator = IncomeCalculator()
    # Calculate net income.
    net_income = calculator.calculate_net_income(income_data)
    print(f"Net Income: {net_income}")

if __name__ == "__main__":
    main()