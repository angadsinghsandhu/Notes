# ================================================================
# File: vendingmachine/dispense_state.py
# Description:
#   Implements the DispenseState behavior.
#   - In DispenseState, payment has been received and the product is ready to be dispensed.
#   - Dispenses the product, updates inventory, and moves to return change.
#
# Steps Covered:
# 4. Determine Core Methods Based on Use Cases.
# ================================================================

from vending_machine_state import VendingMachineState
from product import Product
from coin import Coin
from note import Note

class DispenseState(VendingMachineState):
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine

    def select_product(self, product: Product):
        print("Product already selected. Please collect the dispensed product.")

    def insert_coin(self, coin: Coin):
        print("Payment already made. Please collect the dispensed product.")

    def insert_note(self, note: Note):
        print("Payment already made. Please collect the dispensed product.")

    def dispense_product(self):
        # Dispense the product and update inventory.
        product = self.vending_machine.selected_product
        new_quantity = self.vending_machine.inventory.get_quantity(product) - 1
        self.vending_machine.inventory.update_quantity(product, new_quantity)
        print(f"Product dispensed: {product.name}")
        self.vending_machine.set_state(self.vending_machine.return_change_state)

    def return_change(self):
        print("Please collect the dispensed product first.")