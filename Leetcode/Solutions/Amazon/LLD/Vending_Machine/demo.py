# ================================================================
# File: vendingmachine/vending_machine_demo.py
# Description:
#   Demonstrates the usage of the Vending Machine system.
#   - Creates an instance of VendingMachine (Singleton).
#   - Adds products to the inventory.
#   - Simulates product selection, payment (coins/notes), dispensing, and change return.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 6. Implement Necessary Methods.
# 8. Follow Good Coding Practices.
# ================================================================

from vending_machine import VendingMachine
from product import Product
from coin import Coin
from note import Note

class VendingMachineDemo:
    @staticmethod
    def run():
        vm = VendingMachine.get_instance()

        # Restock the machine with products.
        coke = Product("Coke", 1.5)
        pepsi = Product("Pepsi", 1.5)
        water = Product("Water", 1.0)

        vm.inventory.add_product(coke, 5)
        vm.inventory.add_product(pepsi, 3)
        vm.inventory.add_product(water, 2)

        # Scenario 1: Purchase Coke
        vm.select_product(coke)
        vm.insert_coin(Coin.QUARTER)
        vm.insert_coin(Coin.QUARTER)
        vm.insert_coin(Coin.QUARTER)
        vm.insert_coin(Coin.QUARTER)
        vm.insert_note(Note.FIVE)
        vm.dispense_product()
        vm.return_change()

        # Scenario 2: Purchase Pepsi with insufficient payment first.
        vm.select_product(pepsi)
        vm.insert_coin(Coin.QUARTER)
        vm.dispense_product()  # Expect payment prompt.
        vm.insert_coin(Coin.QUARTER)
        vm.insert_coin(Coin.QUARTER)
        vm.insert_coin(Coin.QUARTER)
        vm.insert_coin(Coin.QUARTER)
        vm.dispense_product()
        vm.return_change()

    if __name__ == "__main__":
        run()

if __name__ == "__main__":
    VendingMachineDemo.run()
