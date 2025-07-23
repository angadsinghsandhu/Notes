# ================================================================
# File: vendingmachine/vending_machine_state.py
# Description:
#   Defines the VendingMachineState interface for different states.
#   - Each concrete state (Idle, Ready, Dispense, Return Change) will implement these methods.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Interfaces and Their Methods.
# ================================================================

from abc import ABC, abstractmethod

class VendingMachineState(ABC):
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine

    @abstractmethod
    def select_product(self, product):
        pass

    @abstractmethod
    def insert_coin(self, coin):
        pass

    @abstractmethod
    def insert_note(self, note):
        pass

    @abstractmethod
    def dispense_product(self):
        pass

    @abstractmethod
    def return_change(self):
        pass