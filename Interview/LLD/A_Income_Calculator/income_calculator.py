# ================================================================
# File: income_calculator/income_calculator.py
# Description:
#   The IncomeCalculator class encapsulates the logic to compute
#   net income based on the provided IncomeData.
#   - It calculates net income = base salary + total bonuses - total deductions.
#
# Steps Covered:
# 4. Determine Core Methods Based on Use Cases.
# 6. Implement Necessary Methods.
# ================================================================

from income_data import IncomeData

class IncomeCalculator:
    def calculate_net_income(self, income_data: IncomeData) -> float:
        total_salary = income_data.salary.amount
        total_bonus = sum(bonus.amount for bonus in income_data.bonuses)
        total_deduction = sum(deduction.amount for deduction in income_data.deductions)
        net_income = total_salary + total_bonus - total_deduction
        return net_income