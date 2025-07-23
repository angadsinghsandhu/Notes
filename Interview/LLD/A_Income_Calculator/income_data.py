# ================================================================
# File: income_calculator/income_data.py
# Description:
#   Aggregates all income components:
#     - Base Salary, Bonuses, and Deductions.
#   - Serves as a data transfer object for the calculator.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# ================================================================

from salary import Salary
from bonus import Bonus
from deduction import Deduction

class IncomeData:
    def __init__(self, salary: Salary, bonuses: list = None, deductions: list = None):
        self.salary = salary
        # Use empty lists as defaults if none provided.
        self.bonuses = bonuses if bonuses is not None else []
        self.deductions = deductions if deductions is not None else []